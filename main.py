import connexion
import pandas as pd
from flask import jsonify
from decouple import Config, RepositoryEnv
from flask_socketio import SocketIO


def _validate_tokenpair(tokenPair: str):
    assert tokenPair == "BTCUSDT", "Temporarly only BTCUSDT token pair is supported"

def _validate_interval(interval: str):
    assert interval == "1d", "Temporarly only 1d interval is supported"

def _validate_times(startTime: int, endTime: int):
    assert startTime >= 1503100799999, "Temporarly cannot start before 18.08.2017 (Unix 1503100799999)"
    assert endTime <= 1693180799999, "Temporarly cannot end after 27.08.2023 (Unix 1693180799999)"
    assert startTime < endTime, "Start time has to be before end time"

def _validate_indicator(indicator: list, columns: list):
    assert indicator in columns, f"Unknown indicator {indicator}, only available are {columns}"


def get_price_for_timerange(
        tokenPair: str,
        interval: str,
        startTime: int,
        endTime: int):
    try:
        _validate_tokenpair(tokenPair)
        _validate_interval(interval)
        _validate_times(startTime, endTime)
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401
    
    data = pd.read_csv(f'data/binance_{tokenPair}_{interval}.csv')
    data = data[['timestamp_close', 'price_close']]
    data = data.rename(columns={'timestamp_close': 'timestamp', 'price_close': 'price'})
    data = data[(data['timestamp'] >= startTime) & (data['timestamp'] <= endTime)]
    return list(data.T.to_dict().values()), 200


def get_indicators_for_timerange(
        tokenPair: str,
        interval: str,
        startTime: int,
        endTime: int,
        indicator: str):
    try:
        _validate_tokenpair(tokenPair)
        _validate_interval(interval)
        _validate_times(startTime, endTime)
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401

    data = pd.read_csv(f'data/binance_{tokenPair}_{interval}.csv')
    
    try:
        _validate_indicator(indicator, list(data.columns))
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401
    
    data = data[['timestamp_close', indicator]]
    data = data.rename(columns={'timestamp_close': 'timestamp'})
    data = data[(data['timestamp'] >= startTime) & (data['timestamp'] <= endTime)]
    return list(data.T.to_dict().values()), 200


config = Config(RepositoryEnv('.env.local'))
app = connexion.FlaskApp(__name__,
        server='tornado',
        specification_dir='',
        options={'swagger_url': '/swagger-ui'})
app.add_api('openapi.yaml')
socketio = SocketIO(app.app)
socketio.run(app.app, port=config.get('PORT'))
