import os
from src.core.model import load_model
from src.interpreter.engine import StoryEngine
from textx.exceptions import TextXSemanticError

def run_console_game():
    current_dir = os.path.dirname(__file__)
    story_path = os.path.join(current_dir, 'examples/lostTemple.story')

    try:
        model = load_model(story_path)
        engine = StoryEngine()
        engine.interpret(model)

        while True:
            room = engine.current_room
            
            print(f"\nLocation: {room.name}")
            print(f"Description: {room.body}")
            print(f"Stats: {engine.variables}")
            print(f"Inventory: {[w.name for w in engine.weapons] + engine.inventory}")
            print("-" * 20)

            if hasattr(room, 'fight') and room.fight:
                print(f" FIGHT TRIGGERED: {room.fight.description}")
                input("Press Enter to start the fight...")
                engine.resolve_fight(room.fight)
                continue

            if not engine.available_options:
                print("\n--- THE END ---")
                break

            print("What do you want to do?")
            for i, opt in enumerate(engine.available_options):
                print(f"{i}. {opt.text}")

            try:
                choice = int(input("\nEnter choice number: "))
                if 0 <= choice < len(engine.available_options):
                    engine.select_option(choice)
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a valid number.")

    except TextXSemanticError as e:
        print(f"FAILED TO START GAME: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_console_game()