from flask import Flask, jsonify


app = Flask(__name__)
app.config.from_object("project.config.Config")


@app.route("/")
def hello_world():
    return jsonify(hello="world")
