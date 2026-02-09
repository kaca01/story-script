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
            
            if engine.fight_mode:
                print(f"\n--- FIGHT: {room.fight.description} ---")
                print(f"Stats: {engine.variables}")
                
                fight_options = engine.build_fight_options()
                for i, opt in enumerate(fight_options):
                    print(f"{i}. {opt['text']}")
                
                try:
                    choice = int(input("\nChoose your attack: "))
                    engine.choose_fight_option(choice)
                except ValueError:
                    print("Please enter a valid number.")
                continue

            # Standardni prikaz sobe (van borbe)
            print(f"\nLocation: {room.name}")
            print(f"Description: {room.body}")
            print(f"Stats: {engine.variables}")
            print(f"Weapons: {[w.name for w in engine.weapons]}")
            print(f"Treasure: {[t.name for t in engine.treasures]}")
            print("-" * 20)

            if hasattr(room, 'fight') and room.fight and not engine.fight_mode:
                engine.build_fight_options() 
                print(f"!!! FIGHT TRIGGERED !!!")
                continue

            if not engine.available_options:
                print("\n--- THE END ---")
                break

            print("What do you want to do?")
            for i, opt in enumerate(engine.available_options):
                print(f"{i}. {opt.text}")

            try:
                choice_str = input("\nEnter choice number: ")
                choice = int(choice_str)
                if 0 <= choice < len(engine.available_options):
                    engine.select_option(choice)
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a valid number.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_console_game()