import tkinter as tk #Python's built-in GUI library
from tkinter import ttk #Modern themed widgets

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
       
        # Habit List
        self.habits = []
       
        # GUI Widgets
        self.label = ttk.Label(root, text="Your Habits:")
        self.label.pack(pady=10)
       
        self.listbox = tk.Listbox(root)
        self.listbox.pack()
       
        self.entry = ttk.Entry(root)
        self.entry.pack(pady=5)
       
        self.add_button = ttk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_button.pack()
       
        self.complete_button = ttk.Button(root, text="Mark Done", command=self.mark_done)
        self.complete_button.pack()

    def add_habit(self):
        habit = self.entry.get()
        if habit:
            self.habits.append({"name": habit, "completed": False})
            self.listbox.insert(tk.END, habit)
            self.entry.delete(0, tk.END)

    def mark_done(self):
        selected = self.listbox.curselection() # Get the selected item index
        if selected:
            index = selected[0]
            self.listbox.itemconfig(index, {'bg':'light green'}) # Change background color
            self.habits[index]["completed"] = True # Mark as completed
    

if __name__ == "__main__":
    root = tk.Tk() # Create the main window
    app = HabitTracker(root) # Create an instance of the HabitTracker class
    root.mainloop() #Run forever