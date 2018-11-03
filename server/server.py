from state import State
from flask import Flask, request

app = Flask(__name__)
state = State()

@app.route('/config', methods=['GET'])
def config():
    ip = request.args.get('ip')
    return state.get_config(ip.lower())

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
