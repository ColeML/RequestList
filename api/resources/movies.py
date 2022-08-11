from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.lookup.movies import VideoLookup
from api.models.movies import MovieRequestModel
from api.models.user import UserModel, UserLevels


class MovieRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Movie Title Required.")
    parser.add_argument('year', type=int, help="Movie's Release Year.")

    id_parser = reqparse.RequestParser()
    id_parser.add_argument('imdb_id', type=str, required=True, help="Movie's IMDB id Required.")

    def get(self) -> (dict, int):
        data = MovieRequest.parser.parse_args()

        title, year = data.get("title"), data.get("year")

        if year:
            movies = VideoLookup.search_by_title_year(title, year, "movie")
        else:
            movies = VideoLookup.search_by_title(title, "movie")

        return movies, 200

    @jwt_required()
    def post(self) -> (dict, int):
        data = MovieRequest.id_parser.parse_args()
        imdb_id = data.get("imdb_id")

        if MovieRequestModel.find_by_id(imdb_id):
            abort(400, message=f"Movie with imdb_id {imdb_id} already requested.")

        movie = VideoLookup.lookup_by_id(imdb_id)
        if not movie:
            abort(404, message=f"Movie with imdb_id {imdb_id} not found.")

        movie = MovieRequestModel(**movie, imdb_id=imdb_id, user=get_jwt_identity())

        movie.save_to_db()

        return movie.json(), 200

    @jwt_required()
    def delete(self) -> (dict, int):
        data = MovieRequest.id_parser.parse_args()

        imdb_id = data.get("imdb_id")

        movie = MovieRequestModel.find_by_id(imdb_id)

        if not movie:
            abort(404, message=f"Request for {imdb_id} does not exist.")

        user = UserModel.find_by_id(get_jwt_identity())
        if get_jwt_identity() is not movie.user_id and user.user_type is not UserLevels.ADMIN:
            abort(401, message=f"Only requesting user or admin can remove the request.")

        movie.delete_from_db()

        return {'message': f'Request deleted successfully.'}, 200


class MovieRequests(Resource):
    @jwt_required()
    def get(self) -> (dict, int):
        user = UserModel.find_by_id(get_jwt_identity())

        if user.user_type is UserLevels.ADMIN:
            requests = [request.json() for request in MovieRequestModel.find_all()]
        else:
            requests = [request.json() for request in MovieRequestModel.find_all_by_user(get_jwt_identity())]

        return {'movie_requests': requests}, 200
