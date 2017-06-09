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

@APP.route('/api/play', methods=['POST'])
def play_video():
    if not request.json \
    or not 'play_at' \
    or not 'time_reference_url':
        abort(400)

    global playback
    playback.play(request.json['play_at'], request.json['time_reference_url'])

    return jsonify({
        'play_at': request.json['play_at'],
        'time_reference_url': request.json['time_reference_url']
    })

@APP.route('/api/stop', methods=['POST'])
def stop_video():
    global playback
    playback.stop()

    return jsonify({
        'stopped': 'OK'
    }), 200

if __name__ == '__main__':
    APP.run(debug=True, port=8003, host='0.0.0.0')