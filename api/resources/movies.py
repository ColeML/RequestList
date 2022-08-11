from typing import Tuple

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort, reqparse

from api.lookup.video import VideoLookup
from api.models.movies import MovieRequestModel
from api.models.user import UserLevels, UserModel


class MovieRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'title', type=str, required=True, help='Movie Title Required.'
    )
    parser.add_argument('year', type=int, help="Movie's Release Year.")

    id_parser = reqparse.RequestParser()
    id_parser.add_argument(
        'imdb_id', type=str, required=True, help="Movie's IMDB id Required."
    )

    def get(self) -> Tuple[dict, int]:
        """GET HTTP method. Retrieves list of movies based on given arguments.

        Search Types:
            title - Searches by movie title.
            title & year - Searched by movie title and release year.

        Returns:
            Tuple[dict, int]: Movies found in search, HTTP status code
        """
        data = MovieRequest.parser.parse_args()

        title, year = data.get('title'), data.get('year')

        if year:
            movies = VideoLookup.search_by_title_year(title, year, 'movie')
        else:
            movies = VideoLookup.search_by_title(title, 'movie')

        return {'movies': movies}, 200

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        """POST HTTP method. Queries movie by imdb id,
        if exists adds the movie request.

        Returns:
            Tuple[dict, int]: The added movie request, HTTP status code
        """
        data = MovieRequest.id_parser.parse_args()
        imdb_id = data.get('imdb_id')

        if MovieRequestModel.find_by_id(imdb_id):
            abort(
                400, message=f'Movie with imdb_id {imdb_id} already requested.'
            )

        movie = VideoLookup.lookup_by_id(imdb_id)
        if not movie:
            abort(404, message=f'Movie with imdb_id {imdb_id} not found.')

        movie = MovieRequestModel(
            **movie, imdb_id=imdb_id, user=int(get_jwt_identity())
        )

        movie.save_to_db()

        return movie.json(), 200

    @jwt_required()
    def delete(self) -> Tuple[dict, int]:
        """DELETE HTTP method, Removes existing request by imdb id if exists.
        Only the requesting user or admin can remove requests.

        Returns:
            Tuple[dict, int]: Delete success message, HTTP status code.
        """
        data = MovieRequest.id_parser.parse_args()

        imdb_id = data.get('imdb_id')

        movie = MovieRequestModel.find_by_id(imdb_id)

        if not movie:
            abort(404, message=f'Request for {imdb_id} does not exist.')

        user = UserModel.find_by_id(get_jwt_identity())
        if (
            get_jwt_identity() is not movie.user_id
            and user.user_type is not UserLevels.ADMIN
        ):
            abort(
                401,
                message='Only requesting user or admin can delete.',
            )

        movie.delete_from_db()

        return {'message': 'Request deleted successfully.'}, 200


class MovieRequests(Resource):
    @jwt_required()
    def get(self) -> Tuple[dict, int]:
        """GET HTTP method, Retrieves a list of the user's movie requests.
        Admin retrieves all existing movie requests.

        Returns:
            Tuple[dict, int]: User's movie requests, HTTP status code
        """
        user = UserModel.find_by_id(get_jwt_identity())

        if user.user_type is UserLevels.ADMIN:
            requests = [
                request.json() for request in MovieRequestModel.find_all()
            ]
        else:
            requests = [
                request.json()
                for request in MovieRequestModel.find_all_by_user(
                    get_jwt_identity()
                )
            ]

        return {'movie_requests': requests}, 200
