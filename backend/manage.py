from flask.cli import FlaskGroup

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(hello="world")



if __name__ == "__main__":
    hello_world()
