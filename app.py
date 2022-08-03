from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api.db import initialize_db, create_db
from api.resources.routes import initialize_routes


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
api = Api(app)

app.config.from_object('api.config.Config')

initialize_db(app)
initialize_routes(api)


@app.before_first_request
def create_tables() -> None:
    create_db()


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
