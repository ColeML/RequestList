from typing import Tuple

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort, reqparse

from api.lookup.music import MusicLookup
from api.models.music import MusicRequestModel
from api.models.user import UserLevels, UserModel


class MusicRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Music Track Title')
    parser.add_argument('album', type=str, help='Music Album')
    parser.add_argument('artist', type=str, help='Music Artist')

    id_parser = reqparse.RequestParser()
    id_parser.add_argument(
        'id', type=int, required=True, help='Deezer_id Required'
    )
    id_parser.add_argument(
        'music_type',
        type=str,
        required=True,
        help='Music type [album, track] Required.',
    )

    def get(self) -> Tuple[dict, int]:
        """GET HTTP method. Retrieves list of movies based on given arguments.

        Search Types:
            title, artist, & album - Search for track by title
                with optional artist and album filters.
            album & artist - Search for album by title
                with optional artist filter.
            artist - Search for all tracks by artist

        Returns:
            Tuple[dict, int]: Movies found in search, HTTP status code
        """
        data = MusicRequest.parser.parse_args()
        title, album, artist = (
            data.get('title'),
            data.get('album'),
            data.get('artist'),
        )

        if not (title or album or artist):
            abort(
                400, message='Requires title, album, or artist to search with.'
            )

        if title:
            music = MusicLookup.search_for_track(title, artist, album)
            if not music:
                abort(
                    404,
                    message=f'Track(s) with - Title {title}, '
                    f'Artist: {artist}, Album: {album} not found.',
                )
        elif album:
            music = MusicLookup.search_for_album(album, artist)
            if not music:
                abort(
                    404,
                    message=f'Album(s) with - Title: {album}, '
                    f'Artist: {artist} not found.',
                )
        else:
            music = MusicLookup.search_for_artist(artist)
            if not music:
                abort(404, message=f'Track(s) from - Artist: {artist}')

        return {'music': music}, 200

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        """POST HTTP method. Queries music by deezer id,
        if exists adds the music request.

        Returns:
            Tuple[dict, int]: The added music request, HTTP status code
        """
        data = MusicRequest.id_parser.parse_args()
        deezer_id, music_type = data.get('id'), data.get('music_type')

        if MusicRequestModel.find_by_deezer_id(deezer_id):
            abort(400, message=f'Request for {deezer_id} already exists.')

        music = MusicLookup.lookup_by_deezer_id(deezer_id, music_type)

        if not music:
            abort(404, message=f'Deezer ID {deezer_id} not found.')

        music = MusicRequestModel(**music, user=get_jwt_identity())

        music.save_to_db()

        return music.json(), 200

    @jwt_required()
    def delete(self) -> Tuple[dict, int]:
        """DELETE HTTP method,
        Removes existing request by deezer id if it exists.
        Only the requesting user or admin can remove requests.

        Returns:
            Tuple[dict, int]: Delete success message, HTTP status code.
        """
        data = MusicRequest.id_parser.parse_args()
        deezer_id = data.get('id')

        music = MusicRequestModel.find_by_deezer_id(deezer_id)

        if not music:
            abort(404, message='Request does not exist.')

        user = UserModel.find_by_id(get_jwt_identity())
        if (
            get_jwt_identity() is not music.user_id
            and user.user_type is not UserLevels.ADMIN
        ):
            abort(
                401,
                message='Only requesting user or admin can'
                ' remove the request.',
            )

        music.delete_from_db()

        return {'message': 'Request deleted successfully.'}, 200


class MusicRequests(Resource):
    @jwt_required()
    def get(self) -> Tuple[dict, int]:
        """GET HTTP method, Retrieves a list of the user's music requests.
        Admin retrieves all existing music requests.

        Returns:
            Tuple[dict, int]: User's music requests, HTTP status code
        """
        user = UserModel.find_by_id(get_jwt_identity())
        if user.user_type is UserLevels.ADMIN:
            requests = [
                request.json() for request in MusicRequestModel.find_all()
            ]
        else:
            requests = [
                request.json()
                for request in MusicRequestModel.find_all_by_user(
                    get_jwt_identity()
                )
            ]

        return {'music_requests': requests}, 200
