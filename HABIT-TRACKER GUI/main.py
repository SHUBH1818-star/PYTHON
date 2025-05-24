import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker Pro")
       
        # Data setup
        self.habits = []
        self.load_habits()
       
        # UI Setup
        self.setup_ui()
       
        # Ensure save on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Initialize all GUI components"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
       
        # Habit List with Streak Display
        self.tree = ttk.Treeview(main_frame, columns=("Name", "Status", "Streak"), show="headings", height=10)
        self.tree.heading("Name", text="Habit Name")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Streak", text="Current Streak")
        self.tree.column("Name", width=200)
        self.tree.column("Status", width=100)
        self.tree.column("Streak", width=80)
        self.tree.pack(pady=10)
        self.refresh_list()
       
        # Entry and Buttons
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=5)
       
        ttk.Label(entry_frame, text="New Habit:").pack(side=tk.LEFT)
        self.entry = ttk.Entry(entry_frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)
       
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
       
        ttk.Button(btn_frame, text="Add Habit", command=self.add_habit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Mark Done", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset Streak", command=self.reset_streak).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_habit).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        """Update the treeview with current habits"""
        for item in self.tree.get_children():
            self.tree.delete(item)
           
        for habit in self.habits:
            status = "✅ Done" if habit["completed"] else "❌ Pending"
            last_done = f"\nLast: {habit.get('last_done', 'Never')}" if "last_done" in habit else ""
            self.tree.insert("", tk.END, values=(
                habit["name"],
                status,
                f"{habit['streak']} days{last_done}"
            ))

    def add_habit(self):
        """Add a new habit to the tracker"""
        habit_name = self.entry.get().strip()
        if habit_name:
            self.habits.append({
                "name": habit_name,
                "completed": False,
                "streak": 0,
                "last_done": None
            })
            self.entry.delete(0, tk.END)
            self.refresh_list()
            self.save_habits()

    def mark_done(self):
        """Mark selected habit as completed and update streak"""
        selection = self.tree.selection()
        if selection:
            index = self.tree.index(selection[0])
            habit = self.habits[index]
           
            today = datetime.now().strftime("%Y-%m-%d")
           
            # Check if already done today
            if habit["last_done"] == today:
                messagebox.showinfo("Info", "You've already completed this today!")
                return
               
            # Update streak
            habit["completed"] = True
            habit["last_done"] = today
            habit["streak"] += 1
           
            self.refresh_list()
            self.save_habits()
            messagebox.showinfo("Great job!", f"Your streak for {habit['name']} is now {habit['streak']} days!")

    def reset_streak(self):
        """Reset streak for selected habit"""
        selection = self.tree.selection()
        if selection:
            index = self.tree.index(selection[0])
            self.habits[index]["streak"] = 0
            self.habits[index]["last_done"] = None
            self.refresh_list()
            self.save_habits()

    def delete_habit(self):
        """Remove selected habit"""
        selection = self.tree.selection()
        if selection:
            index = self.tree.index(selection[0])
            del self.habits[index]
            self.refresh_list()
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
   
    # Set window size and center it
    window_width = 500
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
   
    app = HabitTracker(root)
    root.mainloop()

# This code is a simple Habit Tracker application using Tkinter for the GUI and JSON for data storage.
# It allows users to add habits, mark them as done, reset streaks, and delete habits.