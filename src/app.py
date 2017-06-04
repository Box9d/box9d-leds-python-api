from flask import Flask
import actions.apiactions

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return actions.apiactions.get_home()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')