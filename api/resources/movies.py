from flask_restful import Resource, reqparse

from api.models.movies import MovieRequestModel
from api.lookup.movies import VideoLookup


class MovieRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Movie Title")
    parser.add_argument('year', type=int, help="Movie's Release Year.")
    parser.add_argument('imdb_id', type=str, help="Movie's IMDB id.")

    def get(self) -> (dict, int):
        data = MovieRequest.parser.parse_args()

        title, year = data["title"], data["year"]

        if title and year:
            return VideoLookup.search_by_title_year(title, year, "movie"), 200
        elif title:
            return VideoLookup.search_by_title(title, "movie"), 200
        else:
            return {'message': f'Requires title to search with.'}, 400

    # @jwt_required()
    def post(self) -> (dict, int):
        data = MovieRequest.parser.parse_args()
        title, year, imdb_id = data["title"], data["year"], data["imdb_id"]

        if title and year:
            lookup = VideoLookup.lookup_by_title(title, year, _type="movie")

            if lookup is None:
                return {'message': f'Unable to find movie Title: {title} Year: {year}.'}, 404
        elif imdb_id:
            lookup = VideoLookup.lookup_by_id(imdb_id)
            if lookup is None:
                return {'message': f'Unable to find movie with IMDB id: {imdb_id}'}, 404
        else:
            return {'message': f'Requires Title and Year or IMDB id.'}, 400

        if MovieRequestModel.find_by_id(imdb_id):
            return {'message': f'Movie: {title} year: {year} already requested.'}, 400

        if lookup.get("imdb_id"):
            movie = MovieRequestModel(title, year, lookup["imdb_id"])
        else:
            movie = MovieRequestModel(lookup["title"], lookup["year"], imdb_id)

        print(type(movie))
        movie.save_to_db()

        return movie.json(), 200

    # @jwt_required()
    def delete(self) -> (dict, int):
        data = MovieRequest.parser.parse_args()

        movie = MovieRequestModel.find_by_id(data['imdb_id'])

        if not movie:
            return {'message': f'Request does not exist.'}, 404

        movie.delete_from_db()
        return {'message': f'Request deleted successfully.'}, 200


class MovieRequests(Resource):
    # @jwt_required()
    def get(self) -> (dict, int):
        requests = [request.json() for request in MovieRequestModel.find_all()]
        return {'movie_requests': requests}, 200
