from flask_restful import Resource, reqparse, abort

from api.models.music import MusicRequestModel
from api.lookup.music import MusicLookup


class MusicRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Music Track Title")
    parser.add_argument('album', type=str, help="Music Album")
    parser.add_argument('artist', type=str, help="Music Artist")

    id_parser = reqparse.RequestParser()
    id_parser.add_argument('id', type=int, required=True, help="Deezer_id Required")
    id_parser.add_argument('music_type', type=str, required=True, help="Music type [album, track] Required.")

    def get(self) -> (dict, int):
        data = MusicRequest.parser.parse_args()
        title, album, artist = data.get("title"), data.get("album"), data.get("artist")

        if not (title or album or artist):
            abort(400, message="Requires title, album, or artist to search with.")

        if title:
            music = MusicLookup.search_for_track(title, artist, album)
            if not music:
                abort(404, message=f"Track(s) with - Title {title}, Artist: {artist}, Album: {album} not found.")
        elif album:
            music = MusicLookup.search_for_album(album, artist)
            if not music:
                abort(404, message=f"Album(s) with - Title: {album}, Artist: {artist} not found.")
        else:
            music = MusicLookup.search_for_artist(artist)
            if not music:
                abort(404, message=f"Track(s) from - Artist: {artist}")

        return music, 200

    # @jwt_required()
    def post(self) -> (dict, int):
        data = MusicRequest.id_parser.parse_args()
        deezer_id, music_type = data.get("id"), data.get("music_type")

        if MusicRequestModel.find_by_deezer_id(deezer_id):
            abort(400, message=f"Request for {deezer_id} already exists.")

        music = MusicLookup.lookup_by_deezer_id(deezer_id, music_type)

        if not music:
            abort(404, message=f"Deezer ID {deezer_id} not found.")

        music = MusicRequestModel(**music)

        music.save_to_db()

        return music.json(), 200

    # @jwt_required()
    def delete(self) -> (dict, int):
        # TODO Make sure that user can only delete their own requests, Admins can delete all
        data = MusicRequest.id_parser.parse_args()
        deezer_id = data.get("id")

        music = MusicRequestModel.find_by_deezer_id(deezer_id)

        if not music:
            abort(404, message=f"Request does not exist.")

        music.delete_from_db()

        return {'message': f'Request deleted successfully.'}, 200


class MusicRequests(Resource):
    # @jwt_required()
    def get(self) -> (dict, int):
        # TODO Only return requests from that user unless admin
        requests = [request.json() for request in MusicRequestModel.find_all()]
        return {'music_requests': requests}, 200
