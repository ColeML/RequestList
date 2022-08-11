from api.resources.books import BookRequest, BookRequests
from api.resources.movies import MovieRequest, MovieRequests
from api.resources.shows import ShowRequest, ShowRequests
from api.resources.music import MusicRequest, MusicRequests
from api.resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh


def initialize_routes(api):
    api.add_resource(BookRequest, '/book/request')
    api.add_resource(BookRequests, '/book/requests')
    api.add_resource(MovieRequest, '/movie/request')
    api.add_resource(MovieRequests, '/movie/requests')
    api.add_resource(MusicRequest, '/music/request')
    api.add_resource(MusicRequests, '/music/requests')
    api.add_resource(ShowRequest, '/show/request')
    api.add_resource(ShowRequests, '/show/requests')

    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(UserRegister, '/register')
