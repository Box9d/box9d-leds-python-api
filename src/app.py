from flask import Flask, abort, jsonify, request
from domain.playback import Playback

APP = Flask(__name__)

playback = None

@APP.route('/', methods=['GET'])
def home():
    return 'Hello world'

@APP.route('/api/load', methods=['POST'])
def load_video():
    if not request.json \
    or not 'sqlite_connection_string' \
    or not 'video_id' \
    or not 'frame_rate' in request.json:
        abort(400)

    global playback
    playback = Playback(\
    request.json['sqlite_connection_string'], \
    request.json['video_id'], \
    request.json['frame_rate'])
    playback.load_buffer()

    return jsonify({
        'sqlite_connection_string': request.json['sqlite_connection_string'],
        'video_id': request.json['video_id'],
        'frame_rate': request.json['frame_rate']
        }), 201

@APP.route('/api/stop', methods=['POST'])
def stop_video():
    pass

if __name__ == '__main__':
    APP.run(debug=True, port=8003, host='0.0.0.0')