import json
import os

# --- File Handling Functions ---
def load_habits():
    """Load habits from JSON file or return empty list if file doesn't exist/corrupt"""
    if not os.path.exists("habits.json"):
        return []
   
    try:
        with open("habits.json", "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Warning: Corrupted habits.json. Starting fresh.")
        return []

def save_habits(habits):
    """Save habits to JSON file"""
    with open("habits.json", "w") as f:
        json.dump(habits, f, indent=4)

# --- Main Program ---
def main():
    habits = load_habits()  # <-- CRITICAL: LOAD INITIAL DATA
   
    while True:
        print("\n1. Add Habit\n2. List Habits\n3. Mark Done\n4. Exit")
        choice = input("> ").strip()
       
        if choice == "1":
            name = input("Habit name: ").strip()
            habits.append({"name": name, "completed": False, "streak": 0})
            save_habits(habits)  # Save after adding
           
        elif choice == "2":
            for i, habit in enumerate(habits):
                status = "✅" if habit["completed"] else "❌"
                print(f"{i+1}. {habit['name']} {status} (Streak: {habit['streak']})")
               
        elif choice == "3":
            try:
                num = int(input("Habit number: ")) - 1
                if 0 <= num < len(habits):
                    habits[num]["completed"] = True
                    habits[num]["streak"] += 1
                    save_habits(habits)  # Save after updating
            except ValueError:
                print("Invalid input! Use numbers only.")
               
        elif choice == "4":
            save_habits(habits)  # Final save before exit
            break

if __name__ == "__main__":
    main()  # <-- CRITICAL: RUN THE MAIN FUNCTION