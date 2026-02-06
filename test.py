import os
from src.core.model import load_model
from src.interpreter.engine import StoryEngine

def run_console_game():
    # 1. Path to your .story file
    current_dir = os.path.dirname(__file__)
    story_path = os.path.join(current_dir, 'examples/lostTemple.story')

    # 2. Load model and engine
    try:
        model = load_model(story_path)
        engine = StoryEngine()
        engine.interpret(model)

        # 3. Main Game Loop
        while True:
            room = engine.current_room
            
            # Print Room Info
            print(f"\nLocation: {room.name}")
            print(f"Description: {room.body}")
            print(f"Stats: {engine.variables}")
            print(f"Inventory: {[w.name for w in engine.weapons] + engine.inventory}")
            print("-" * 20)

            # Check if it's a fight room
            if hasattr(room, 'fight') and room.fight:
                print(f" FIGHT TRIGGERED: {room.fight.description}")
                input("Press Enter to start the fight...")
                engine.resolve_fight(room.fight)
                continue # Go to next loop to show the win/loss room

            # Check for Game Over (no options and no fight)
            if not engine.available_options:
                print("\n--- THE END ---")
                break

            # Print Options
            print("What do you want to do?")
            for i, opt in enumerate(engine.available_options):
                print(f"{i}. {opt.text}")

            # Get User Input
            try:
                choice = int(input("\nEnter choice number: "))
                if 0 <= choice < len(engine.available_options):
                    engine.select_option(choice)
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a valid number.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_console_game()