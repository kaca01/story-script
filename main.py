from src.interpreter.engine import run_engine
from src.core.model import load_model
import os

def main():
    path = os.path.join(os.path.dirname(__file__), 'examples/lostTemple.story')
    
    try:
        model = load_model(path)
        print("✅ Uspešno!")
        for room in model.rooms:
            print(f"Pronađena soba: {room.name} - {room.header}")
    except Exception as e:
        print(f"❌ Greška: {e}")

if __name__ == "__main__":
    # main()
    run_engine(False)