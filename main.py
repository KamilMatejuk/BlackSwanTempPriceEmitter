import connexion
from flask import jsonify
from decouple import Config, RepositoryEnv
from flask_socketio import SocketIO


def get_price_from_timerange(
        tokenPair: str,
        interval: str,
        startTime: int,
        endTime: int):
    try:
        assert tokenPair == "BTCUSDT", "Temporarly only BTCUSDT token pair is supported"
        assert interval == "1d", "Temporarly only 1d interval is supported"
        assert startTime >= 1503014400000, "Temporarly cannot start before 18.08.2017 (Unix 1503014400000)"
        assert endTime <= 1693094400000, "Temporarly cannot end after 27.08.2023 (Unix 1693094400000)"
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401

    return {}, 200


config = Config(RepositoryEnv('.env.local'))
app = connexion.FlaskApp(__name__,
        server='tornado',
        specification_dir='',
        options={'swagger_url': '/swagger-ui'})
app.add_api('openapi.yaml')
socketio = SocketIO(app.app)
socketio.run(app.app, port=config.get('PORT'))
