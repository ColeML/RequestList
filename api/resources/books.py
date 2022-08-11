from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, abort

from api.models.books import BookRequestModel
from api.lookup.books import BookLookup
from api.models.user import UserModel, UserLevels


class BookRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help="Book's Title")
    parser.add_argument('author', type=str, help="Book's Author")
    parser.add_argument('year', type=int, help="Book's Release Year.")

    isbn_parser = reqparse.RequestParser()
    isbn_parser.add_argument('isbn', type=str, required=True, help="Book's isbn (10 or 13) Required")
    isbn_parser.add_argument('book_format', type=str, required=True,
                             help="Desired Media Format Required - [ebook, audiobook]")

    def get(self) -> (dict, int):
        data = self.parser.parse_args()
        title, year, author = data.get("title"), data.get("year"), data.get("author")

        if not (title or author):
            abort(400, message=f"Title or Author required for lookup.")

        if title and year:
            books = BookLookup.search_by_title_year(title, year)
        elif title:
            books = BookLookup.search_by_title(title)
        else:
            books = BookLookup.search_by_author(author)

        return books, 200

    @jwt_required()
    def post(self) -> (dict, int):
        data = BookRequest.isbn_parser.parse_args()

        isbn, book_format = data.get("isbn"), data.get("book_format")

        if BookRequestModel.find_by_isbn(isbn, book_format):
            abort(400, message=f"Request for {book_format} with isbn {isbn} already exists.")

        lookup = BookLookup.lookup_by_isbn(isbn)

        if not lookup:
            abort(404, message=f"Book with with isbn {isbn} not found.")

        book = BookRequestModel(**lookup, book_format=book_format, user=get_jwt_identity())
        book.save_to_db()

        return book.json(), 200

    @jwt_required()
    def delete(self) -> (dict, int):
        data = BookRequest.isbn_parser.parse_args()

        isbn, book_type = data.get("isbn"), data.get("book_format")
        book = BookRequestModel.find_by_isbn(isbn, book_type)

        if not book:
            abort(404, message=f"{book_type} request with {isbn} does not exist.")

        user = UserModel.find_by_id(get_jwt_identity())
        if get_jwt_identity() is not book.user and user.user_type is not UserLevels.ADMIN:
            abort(401, message=f"Only requesting user or admin can remove the request.")

        book.delete_from_db()

        return {'message': f"Request deleted successfully."}, 200


class BookRequests(Resource):
    @jwt_required()
    def get(self) -> (dict, int):
        user = UserModel.find_by_id(get_jwt_identity())
        if user.user_type is UserLevels.ADMIN:
            requests = [request.json() for request in BookRequestModel.find_all()]
        else:
            requests = [request.json() for request in BookRequestModel.find_all_by_user(get_jwt_identity())]

        return {'book_requests': requests}, 200
