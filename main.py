from src.interpreter.engine import StoryEngine
from src.core.model import load_model
import os

def main(debug=False):
    path = os.path.join(os.path.dirname(__file__), 'examples/lostTemple.story')
    story_model = load_model(path, debug)
    story_engine = StoryEngine()
    story_engine.interpret(story_model)

if __name__ == "__main__":
    main()
