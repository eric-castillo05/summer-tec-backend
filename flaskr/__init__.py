from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello, World!"

    return app