from flask_restful import Resource, reqparse

from api.models.music import MusicRequestModel
from api.lookup.music import MusicLookup


class MusicRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Music Track Title")
    parser.add_argument('album', type=str, help="Music Album")
    parser.add_argument('artist', type=str, help="Music Artist")
    parser.add_argument('id', type=int, help="Deezer music id.")
    parser.add_argument('music_type', type=str, help="Music type [album, track]")

    def get(self) -> (dict, int):
        data = MusicRequest.parser.parse_args()
        title = data.get("title")
        album = data.get("album")
        artist = data.get("artist")
        deezer_id = data.get("id")
        music_type = data.get("music_type")

        if deezer_id and music_type:
            music = MusicLookup.lookup_by_deezer_id(deezer_id, music_type)
            if not music:
                return {'message': f"Unable to find {music_type} with - Deezer Id: {deezer_id}"}, 400
        elif title:
            music = MusicLookup.search_for_track(title, artist, album)
            if not music:
                return {'message': f"Unable to find track(s) with - Title {title}, Artist: {artist}, Album: {album}"}, 400
        elif album:
            music = MusicLookup.search_for_album(album, artist)
            if not music:
                return {'message': f"Unable to find album(s) with - Title: {album}, Artist: {artist}"}, 400
        elif artist:
            music = MusicLookup.search_for_artist(artist)
            if not music:
                return {'message': f"Unable to find track(s) with - Artist: {artist}"}, 400
        else:
            return {'message': f'Requires title, album, or artist, or deezer id to search with.'}, 400

        for track in music:
            if track.get("release_date"):
                track["release_date"] = str(music.get("release_date"))

        return music, 200

    # @jwt_required()
    def post(self) -> (dict, int):
        data = MusicRequest.parser.parse_args()
        deezer_id = data["id"]
        music_type = data["music_type"]

        if deezer_id and music_type:
            music = MusicLookup.lookup_by_deezer_id(deezer_id, music_type)
            if not music:
                return {'message': f"Unable to find {music_type} with - Deezer Id: {deezer_id}"}, 400
            music = MusicRequestModel(**music)
        else:
            return {'message': f'Requires deezer id.'}, 400

        music.save_to_db()

        return music.json(), 200

    # @jwt_required()
    def delete(self) -> (dict, int):
        # TODO Make sure that user can only delete their own requests, Admins can delete all
        data = MusicRequest.parser.parse_args()

        deezer_id = data.get("id")

        if not deezer_id:
            return {'message': f"Requires deezer id for request lookup."}, 400

        music = MusicRequestModel.find_by_deezer_id(deezer_id)

        if not music:
            return {'message': f'Request does not exist.'}, 404

        music.delete_from_db()
        return {'message': f'Request deleted successfully.'}, 200


class MusicRequests(Resource):
    # @jwt_required()
    def get(self) -> (dict, int):
        # TODO Only return requests from that user unless admin
        requests = [request.json() for request in MusicRequestModel.find_all()]
        return {'music_requests': requests}, 200
