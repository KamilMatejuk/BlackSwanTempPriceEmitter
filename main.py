import connexion
from decouple import Config, RepositoryEnv
from flask_socketio import SocketIO


def get_price_from_timerange(
        tokenPair: str,
        interval: str,
        startTime: int,
        endTime: int):
    return {}, 200


config = Config(RepositoryEnv('.env.local'))
app = connexion.FlaskApp(__name__,
        server='tornado',
        specification_dir='',
        options={'swagger_url': '/swagger-ui'})
app.add_api('openapi.yaml')
socketio = SocketIO(app.app)
socketio.run(app.app, port=config.get('PORT'))
