from flask_restful import Resource, reqparse, abort

from api.models.movies import MovieRequestModel
from api.lookup.movies import VideoLookup


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

    # @jwt_required()
    def post(self) -> (dict, int):
        data = MovieRequest.id_parser.parse_args()
        imdb_id = data.get("imdb_id")

        if MovieRequestModel.find_by_id(imdb_id):
            abort(400, message=f"Movie with imdb_id {imdb_id} already requested.")

        movie = VideoLookup.lookup_by_id(imdb_id)
        if not movie:
            abort(404, message=f"Movie with imdb_id {imdb_id} not found.")

        movie = MovieRequestModel(**movie, imdb_id=imdb_id)

        movie.save_to_db()

        return movie.json(), 200

    # @jwt_required()
    def delete(self) -> (dict, int):
        data = MovieRequest.id_parser.parse_args()

        imdb_id = data.get("imdb_id")

        movie = MovieRequestModel.find_by_id(imdb_id)

        if not movie:
            abort(404, message=f"Request for {imdb_id} does not exist.")

        movie.delete_from_db()

        return {'message': f'Request deleted successfully.'}, 200


class MovieRequests(Resource):
    # @jwt_required()
    def get(self) -> (dict, int):
        requests = [request.json() for request in MovieRequestModel.find_all()]
        return {'movie_requests': requests}, 200
