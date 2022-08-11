from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, abort

from api.lookup.movies import VideoLookup
from api.models.shows import ShowRequestModel
from api.models.user import UserModel, UserLevels


class ShowRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Show's Title Required")
    parser.add_argument('year', type=int, help="Show's Release Year.")

    id_parser = reqparse.RequestParser()
    id_parser.add_argument('imdb_id', type=str, required=True, help="Show's IMDB id.")

    def get(self) -> (dict, int):
        data = ShowRequest.parser.parse_args()
        title, year = data.get("title"), data.get("year")

        if year:
            shows = VideoLookup.search_by_title_year(title, year, "series")
        else:
            shows = VideoLookup.search_by_title(title, "series")

        return shows, 200

    @jwt_required()
    def post(self) -> (dict, int):
        data = ShowRequest.id_parser.parse_args()
        imdb_id = data.get("imdb_id")

        if ShowRequestModel.find_by_id(imdb_id):
            abort(400, message=f'Show with imdb_id {imdb_id} already requested.')

        show = VideoLookup.lookup_by_id(imdb_id)
        if show is None:
            abort(404,  message=f'Unable to find show with IMDB id: {imdb_id}')

        show = ShowRequestModel(**show, imdb_id=imdb_id, user=get_jwt_identity())

        show.save_to_db()

        return show.json(), 200

    @jwt_required()
    def delete(self) -> (dict, int):
        data = ShowRequest.id_parser.parse_args()
        imdb_id = data.get("imdb_id")

        show = ShowRequestModel.find_by_id(imdb_id)

        if not show:
            abort(404, message=f"Request for {imdb_id} does not exists.")

        user = UserModel.find_by_username(get_jwt_identity())
        if get_jwt_identity() is not show.user and user.user_type is not UserLevels.ADMIN:
            abort(401, message=f"Only requesting user or admin can remove the request.")

        show.delete_from_db()

        return {'message': f'Request deleted successfully.'}, 200


class ShowRequests(Resource):
    @jwt_required()
    def get(self) -> (dict, int):
        user = UserModel.find_by_username(get_jwt_identity())
        if user.user_type is UserLevels.ADMIN:
            requests = [request.json() for request in ShowRequestModel.find_all()]
        else:
            requests = [request.join() for request in ShowRequestModel.find_all_by_user(get_jwt_identity())]

        return {'show_requests': requests}, 200
