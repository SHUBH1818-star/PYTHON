import tkinter as tk
from tkinter import ttk
import json
import os

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker Pro")
       
        # Data setup
        self.habits = []
        self.load_habits()  # Load saved habits
       
        # UI Setup
        self.setup_ui()
       
        # Ensure save on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Initialize all GUI components"""
        # Frame for organization
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
       
        # Habit List
        self.listbox = tk.Listbox(main_frame, height=10, width=50)
        self.listbox.pack(pady=10)
        self.refresh_listbox()
       
        # Entry Field
        self.entry = ttk.Entry(main_frame, width=30)
        self.entry.pack(pady=5)
       
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
       
        ttk.Button(btn_frame, text="Add Habit", command=self.add_habit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Mark Done", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_habit).pack(side=tk.LEFT, padx=5)

    def refresh_listbox(self):
        """Update the listbox with current habits"""
        self.listbox.delete(0, tk.END)
        for habit in self.habits:
            self.listbox.insert(tk.END, habit["name"])
            if habit["completed"]:
                self.listbox.itemconfig(tk.END, {'bg': 'light green'})

    def add_habit(self):
        """Add a new habit to the tracker"""
        habit_name = self.entry.get().strip()
        if habit_name:
            self.habits.append({
                "name": habit_name,
                "completed": False,
                "streak": 0
            })
            self.entry.delete(0, tk.END)
            self.refresh_listbox()
            self.save_habits()

    def mark_done(self):
        """Mark selected habit as completed"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.habits[index]["completed"] = True
            self.habits[index]["streak"] += 1
            self.refresh_listbox()
            self.save_habits()

    def delete_habit(self):
        """Remove selected habit"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            del self.habits[index]
            self.refresh_listbox()
            self.save_habits()

    def load_habits(self):
        """Load habits from JSON file"""
        try:
            if os.path.exists("habits.json"):
                with open("habits.json", "r") as f:
                    self.habits = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading habits: {e}. Starting fresh.")
            self.habits = []

    def save_habits(self):
        """Save habits to JSON file"""
        with open("habits.json", "w") as f:
            json.dump(self.habits, f, indent=4)

    def on_close(self):
        """Handle window close event"""
        self.save_habits()
        self.root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

