from src.interpreter.engine import StoryEngine
from src.core.model import load_model
import os
from app import app

def main(debug=False):
    path = os.path.join(os.path.dirname(__file__), 'examples/lostTemple.story')
    story_model = load_model(path, debug)
    story_engine = StoryEngine()
    story_engine.interpret(story_model)
    app.run(debug=True)


if __name__ == "__main__":
    main()
