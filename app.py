from flask import Flask, send_from_directory, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api.db import initialize_db, create_db, jwt_redis_blocklist
from api.resources.routes import initialize_routes


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
api = Api(app)
app.config.from_object('api.config.Config')
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@app.before_first_request
def create_tables() -> None:
    create_db()


@jwt.expired_token_loader
def expired_token_callback(callback):
    return jsonify({'Description': 'The token has expired.', 'Error': 'token_expired'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({'Description': 'Signature Verification Failed.', 'Error': 'invalid_token'}), 401


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({'Description': 'Request does not contain an access token.', 'Error': 'unauthorized'}), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(callback):
    return jsonify({'Description': 'Fresh Token Required.', 'Error': 'stale_token'}), 401


@jwt.revoked_token_loader
def revoked_token_callback(callback):
    return jsonify({'Description': 'Token has been revoked.', 'Error': 'revoked_token'}), 401


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
