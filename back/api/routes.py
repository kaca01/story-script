import os

from flask import Blueprint

from src.interpreter.service.service import StoryService

dsl_bp = Blueprint("dsl", __name__)

path = os.path.join(os.path.dirname(__file__), '../examples/lostTemple.story')
story_service = StoryService(path)

@dsl_bp.route("/", methods=["GET"])
def index():
    return {"message": "Welcome to the Story DSL API"}


@dsl_bp.route("/state", methods=["GET"])
def get_state():
    res = story_service.get_view_state()
    print(res)
    return res