from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os

from db import db
from resources.books import BookRequest, BookRequests
from resources.movies import MovieRequest, MovieRequests
from resources.shows import ShowRequest, ShowRequests
# from resources.music import SongRequest, SongRequests
from resources.user import UserRegister, User, UserLogin, TokenRefresh


app = Flask(__name__)

uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "temp"  # Move to secure
api = Api(app)


@app.before_first_request
def create_tables() -> None:
    db.create_all()


jwt = JWTManager(app)

# Set Endpoints
api.add_resource(BookRequest, '/book/request')
api.add_resource(BookRequests, '/book/requests')
api.add_resource(MovieRequest, '/movie/request')
api.add_resource(MovieRequests, '/movie/requests')
api.add_resource(ShowRequest, '/show/request')
api.add_resource(ShowRequests, '/show/requests')
# api.add_resource(SongRequest, '/song/request')
# api.add_resource(SongRequests, '/song/requests')

api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
