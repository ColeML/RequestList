from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from api.models.books import BookRequestModel
from api.lookup.books import BookLookup


class BookRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Book's Title")
    parser.add_argument('year', type=int, help="Book's Release Year.")
    parser.add_argument('isbn_10', type=int, help="Books ISBN_13.")
    parser.add_argument('isbn_13', type=int, help="Books ISBN_13")
    parser.add_argument('book_format', type=str, default="ebook", help="Desired Media Format - [ebook, audiobook]")

    def get(self) -> (dict, int):
        data = self.parser.parse_args()

        if data["title"] and data["year"]:
            return BookLookup.search_by_title_year(data["title"], data["year"]), 200
        elif data["title"]:
            return BookLookup.search_by_title(data["title"]), 200
        else:
            return {'message': f'Requires book title to search with.'}, 400

    @jwt_required()
    def post(self) -> (dict, int):
        data = BookRequest.parser.parse_args()

        isbn_10, isbn_13, book_format = data["isbn_10"], data["isbn_13"], data["book_format"]

        if isbn_10:
            lookup = BookLookup.lookup_by_isbn(isbn_10)
        elif isbn_13:
            lookup = BookLookup.lookup_by_isbn(isbn_13)
        else:
            return {'message': "Book's isbn required."}, 400

        if not lookup:
            return {'message': f"Unable to find book."}, 400

        book = BookRequestModel(**lookup, book_format=book_format)

        return book.json(), 200

    @jwt_required()
    def delete(self) -> (dict, int):
        data = BookRequest.parser.parse_args()

        isbn_10, isbn_13 = data["isbn_10"], data["isbn_13"]

        if isbn_10:
            book = BookRequestModel.find_by_isbn10(isbn_10)
        elif isbn_13:
            book = BookRequestModel.find_by_isbn13(isbn_13)
        else:
            return {'message': f"Requires isbn."}, 400

        if not book:
            return {'message': f"Request does not exist."}, 404

        book.delete_from_db()
        return {'message': f"Request deleted successfully."}, 200


class BookRequests(Resource):
    def get(self) -> (dict, int):
        requests = [request for request in BookRequestModel.find_all()]
        return {'book_requests': requests}, 200
