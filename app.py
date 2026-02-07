import os
from flask import Flask
from src.interpreter.engine import StoryEngine
from api.routes import dsl_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:4200"}},
    supports_credentials=True
)
app.register_blueprint(dsl_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
