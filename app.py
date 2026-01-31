import os
from flask import Flask
from src.interpreter.engine import StoryEngine
from api.routes import dsl_bp

app = Flask(__name__)
app.register_blueprint(dsl_bp, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True)
