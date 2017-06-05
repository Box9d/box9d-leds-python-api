from flask import Flask
import actions.apiactions

APP = Flask(__name__)

@APP.route('/', methods=['GET'])
def home():
    return actions.apiactions.get_home()

if __name__ == '__main__':
    APP.run(debug=True, port=8003, host='0.0.0.0')