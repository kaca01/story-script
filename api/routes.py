import os

from flask import Blueprint

from src.core.model import load_model
from src.interpreter.engine import StoryEngine

dsl_bp = Blueprint("dsl", __name__)

path = os.path.join(os.path.dirname(__file__), '../examples/lostTemple.story')
story_model = load_model(path, False)
story_engine = StoryEngine()
story_engine.interpret(story_model)

@dsl_bp.route("/", methods=["GET"])
def index():
    return {"message": "Welcome to the Story DSL API"}


@dsl_bp.route("/state", methods=["GET"])
def get_state():
    res = story_engine.get_view_state()
    print(res)
    return res