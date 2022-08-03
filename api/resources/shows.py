from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from api.models.shows import ShowRequestModel
from api.lookup.movies import VideoLookup


class ShowRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Show Title")
    parser.add_argument('year', type=int, help="Show's Release Year.")
    parser.add_argument('imdb_id', type=str, help="Show's IMDB id.")

    def get(self) -> (dict, int):
        data = ShowRequest.parser.parse_args()

        title, year = data["title"], data["year"]

        if title and year:
            return VideoLookup.search_by_title_year(title, year, "series"), 200
        elif title:
            return VideoLookup.search_by_title(title, "series"), 200
        else:
            return {'message': f'Requires title to search with.'}, 400

    @jwt_required()
    def post(self) -> (dict, int):
        data = ShowRequest.parser.parse_args()
        title, year, imdb_id = data["title"], data["year"], data["imdb_id"]

        if title and year:
            lookup = VideoLookup.lookup_by_title(title, year, _type="show")

            if lookup is None:
                return {'message': f'Unable to find show Title: {title} Year: {year}.'}, 404

            imdb_id = lookup["imdb_id"]
        elif imdb_id:
            lookup = VideoLookup.lookup_by_id(imdb_id)
            if lookup is None:
                return {'message': f'Unable to find show with IMDB id: {imdb_id}'}, 404
        else:
            return {'message': f'Requires Title and Year or IMDB id.'}, 400

        if ShowRequestModel.find_by_id(imdb_id):
            return {'message': f'Show: {title} year: {year} already requested.'}, 400

        show = ShowRequestModel(title, year, imdb_id)
        show.save_to_db()

        return show.json(), 200

    @jwt_required()
    def delete(self) -> (dict, int):
        data = ShowRequest.parser.parse_args()

        show = ShowRequestModel.find_by_id(data['imdb_id'])

        if not show:
            return {'message': f'Request does not exist.'}, 404

        show.delete_from_db()
        return {'message': f'Request deleted successfully.'}, 200


class ShowRequests(Resource):
    @jwt_required()
    def get(self) -> (dict, int):
        requests = [request.json() for request in ShowRequestModel.find_all()]
        return {'show_requests': requests}, 200
