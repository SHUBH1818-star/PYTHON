import tkinter as tk #Python's built-in GUI library
from tkinter import ttk #Modern themed widgets
import json #For saving and loading habits
import os #For file path operations
class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
       
        # Habit List
        self.habits = []
        self.create_widgets()
        self.load_habits() # Load habits from file on startup
        # GUI Widgets
        self.label = ttk.Label(root, text="Your Habits:")
        self.label.pack(pady=10)
       
        self.listbox = tk.Listbox(root)
        self.listbox.pack()
       
        self.entry = ttk.Entry(root)
        self.entry.pack(pady=5)
       
        self.add_button = ttk.Button(
            root,
            text="Add Habit",
            command=self.add_habit
            )
        self.add_button.pack()
       
        self.complete_button = ttk.Button(root, text="Mark Done", command=self.mark_done)
        self.complete_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close event

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Your Habits:")
        self.listbox = tk.Listbox(self.root)
        self.entry = ttk.Entry(self.root)
        self.add_button = ttk.Button(
            self.root,
            text="Add Habit",
            command=self.add_habit)
    def add_habit(self):
        print("Button clicked")
        habit = self.entry.get("")
        if habit:
            print(f"Adding habit: {habit}")
            self.habits.append({"name": habit, "completed": False})
            self.listbox.insert(tk.END, habit)
            self.entry.delete(0, tk.END)
            self.save_habits()

    def mark_done(self):
        selected = self.listbox.curselection() # Get the selected item index
        if selected:
            index = selected[0]
            self.listbox.itemconfig(index, {'bg':'light green'}) # Change background color
            self.habits[index]["completed"] = True 
            self.save_habits()# Mark as completed
    def load_habits(self):
        """Load habits from JSON file on startup"""
        try:
            with open("habits.json", "r") as f:
                self.habits = json.load(f)
            # Populate the Listbox
            for habit in self.habits:
                self.listbox.insert(tk.END, habit["name"])
                if habit["completed"]:
                    last_index = self.listbox.size() - 1
                    self.listbox.itemconfig(last_index, {'bg': 'light green'})
        except (FileNotFoundError, json.JSONDecodeError):
            self.habits = []  # Start fresh if file doesn't exist or is corrupt
    def save_habits(self):
        """Save habits to JSON file"""
        with open("habits.json", "w") as f:
            json.dump(self.habits, f, indent=4)
    def on_closing(self):
        self.save_habits() # Save habits before closing
        self.root.destroy()


    

if __name__ == "__main__":
    root = tk.Tk() # Create the main window
    app = HabitTracker(root) # Create an instance of the HabitTracker class
    root.mainloop() #Run forever