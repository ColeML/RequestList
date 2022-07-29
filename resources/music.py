from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.music import MusicRequestModel
from lookup.music import MusicLookup


class MusicRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Music Title")
    parser.add_argument('year', type=int, help="Music's Release Year.")

    def get(self) -> (dict, int):
        data = MusicRequest.parser.parse_args()
        title, year = data["title"], data["year"]

        if title and year:
            return MusicLookup.search_by_title_year(title, year), 200
        elif title:
            return MusicLookup.search_by_title(title), 200
        else:
            return {'message': f'Requires title to search with.'}, 400

    # @jwt_required()
    def post(self) -> (dict, int):
        data = MusicRequest.parser.parse_args()
        title, year = data["title"], data["year"]

        if title and year:
            lookup = MusicLookup.lookup_by_title(title)
            if lookup is None:
                return {'message': f'Unable to find music Title: {title} Year: {year}.'}, 404
        else:
            return {'message': f'Requires Title and Year'}, 400

        if lookup.get("imdb_id"):
            movie = MusicRequestModel(title, year)
        else:
            movie = MusicRequestModel(lookup["title"], lookup["year"])

        movie.save_to_db()

        return movie.json(), 200

    # @jwt_required()
    def delete(self) -> (dict, int):
        data = MusicRequest.parser.parse_args()
        movie = MusicRequestModel.find_by_id(data['imdb_id'])

        if not movie:
            return {'message': f'Request does not exist.'}, 404

        movie.delete_from_db()
        return {'message': f'Request deleted successfully.'}, 200


class MusicRequests(Resource):
    # @jwt_required()
    def get(self) -> (dict, int):
        requests = [request.json() for request in MusicRequestModel.find_all()]
        return {'music_requests': requests}, 200
