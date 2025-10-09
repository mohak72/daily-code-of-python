import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from cli_todo import TodoList
import json

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Manager")
        self.root.geometry("800x600")
        
        # Initialize todo list
        self.todo_list = TodoList()
        
        # Theme configuration
        self.setup_theme()
        
        # Create GUI elements
        self.setup_gui()
        
        # Load todos
        self.load_todos()
        
    def setup_theme(self):
        """Configure the application theme"""
        style = ttk.Style()
        style.configure("Todo.TFrame", padding=5)
        style.configure("Todo.TLabel", padding=2)
        style.configure("Priority.high.TLabel", foreground="red")
        style.configure("Priority.medium.TLabel", foreground="orange")
        style.configure("Priority.low.TLabel", foreground="green")
        
    def setup_gui(self):
        """Set up the main GUI elements"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left side - Todo list
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Todos", padding="5")
        self.list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Filters frame
        filters_frame = ttk.Frame(self.list_frame)
        filters_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Status filter
        self.status_var = tk.StringVar(value="all")
        ttk.Label(filters_frame, text="Status:").pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(filters_frame, text="All", variable=self.status_var, 
                       value="all", command=self.apply_filters).pack(side=tk.LEFT)
        ttk.Radiobutton(filters_frame, text="Active", variable=self.status_var,
                       value="active", command=self.apply_filters).pack(side=tk.LEFT)
        ttk.Radiobutton(filters_frame, text="Completed", variable=self.status_var,
                       value="completed", command=self.apply_filters).pack(side=tk.LEFT)
        
        # Todo list
        self.todo_tree = ttk.Treeview(self.list_frame, columns=("ID", "Title", "Due", "Priority", "Category"),
                                    show="headings", selectmode="browse")
        self.todo_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure columns
        self.todo_tree.heading("ID", text="ID")
        self.todo_tree.heading("Title", text="Title")
        self.todo_tree.heading("Due", text="Due Date")
        self.todo_tree.heading("Priority", text="Priority")
        self.todo_tree.heading("Category", text="Category")
        
        self.todo_tree.column("ID", width=50)
        self.todo_tree.column("Title", width=200)
        self.todo_tree.column("Due", width=100)
        self.todo_tree.column("Priority", width=80)
        self.todo_tree.column("Category", width=100)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, 
                                  command=self.todo_tree.yview)
        tree_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.todo_tree["yscrollcommand"] = tree_scroll.set
        
        # Right side - Todo details
        self.details_frame = ttk.LabelFrame(self.main_frame, text="Todo Details", padding="5")
        self.details_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Title
        ttk.Label(self.details_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.details_frame, textvariable=self.title_var)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Description
        ttk.Label(self.details_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.description_text = tk.Text(self.details_frame, height=4, width=30)
        self.description_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Due date
        ttk.Label(self.details_frame, text="Due Date:").grid(row=2, column=0, sticky=tk.W)
        self.due_date_var = tk.StringVar()
        self.due_date_entry = ttk.Entry(self.details_frame, textvariable=self.due_date_var)
        self.due_date_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(self.details_frame, text="Pick Date", 
                  command=self.show_calendar).grid(row=2, column=2)
        
        # Priority
        ttk.Label(self.details_frame, text="Priority:").grid(row=3, column=0, sticky=tk.W)
        self.priority_var = tk.StringVar(value="medium")
        priority_frame = ttk.Frame(self.details_frame)
        priority_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Radiobutton(priority_frame, text="Low", variable=self.priority_var,
                       value="low").pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Medium", variable=self.priority_var,
                       value="medium").pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="High", variable=self.priority_var,
                       value="high").pack(side=tk.LEFT)
        
        # Category
        ttk.Label(self.details_frame, text="Category:").grid(row=4, column=0, sticky=tk.W)
        self.category_var = tk.StringVar(value="general")
        self.category_combo = ttk.Combobox(self.details_frame, textvariable=self.category_var)
        self.category_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Buttons
        button_frame = ttk.Frame(self.details_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="New Todo", 
                  command=self.new_todo).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=self.save_todo).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Complete", 
                  command=self.complete_todo).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", 
                  command=self.delete_todo).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.rowconfigure(1, weight=1)
        self.details_frame.columnconfigure(1, weight=1)
        
        # Bind selection event
        self.todo_tree.bind("<<TreeviewSelect>>", self.on_select_todo)
        
    def load_todos(self):
        """Load and display todos in the tree view"""
        # Clear existing items
        for item in self.todo_tree.get_children():
            self.todo_tree.delete(item)
        
        # Update category list
        categories = self.todo_list.get_categories()
        self.category_combo["values"] = ["general"] + [c for c in categories if c != "general"]
        
        # Apply filters
        self.apply_filters()
        
    def apply_filters(self):
        """Apply filters and update the todo list"""
        status = self.status_var.get()
        
        if status == "all":
            todos = self.todo_list.get_todos()
        elif status == "active":
            todos = self.todo_list.get_todos(filter_completed=False)
        else:  # completed
            todos = self.todo_list.get_todos(filter_completed=True)
        
        # Clear existing items
        for item in self.todo_tree.get_children():
            self.todo_tree.delete(item)
        
        # Add filtered todos
        for todo in todos:
            self.todo_tree.insert("", "end", values=(
                todo["id"],
                todo["title"],
                todo["due_date"] or "",
                todo["priority"],
                todo["category"]
            ))
    
    def show_calendar(self):
        """Show calendar popup for date selection"""
        top = tk.Toplevel(self.root)
        top.title("Select Due Date")
        
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=10, pady=10)
        
        def set_date():
            self.due_date_var.set(cal.get_date())
            top.destroy()
        
        ttk.Button(top, text="OK", command=set_date).pack(pady=5)
    
    def new_todo(self):
        """Clear the form for a new todo"""
        self.title_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.due_date_var.set("")
        self.priority_var.set("medium")
        self.category_var.set("general")
        self.todo_tree.selection_remove(self.todo_tree.selection())
    
    def save_todo(self):
        """Save the current todo"""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please enter a title.")
            return
        
        description = self.description_text.get("1.0", tk.END).strip()
        due_date = self.due_date_var.get().strip()
        priority = self.priority_var.get()
        category = self.category_var.get()
        
        selection = self.todo_tree.selection()
        if selection:  # Update existing todo
            todo_id = int(self.todo_tree.item(selection[0])["values"][0])
            self.todo_list.update_todo(
                todo_id, title, description, due_date, priority, category
            )
        else:  # New todo
            self.todo_list.add_todo(title, description, due_date, priority, category)
        
        self.load_todos()
        messagebox.showinfo("Success", "Todo saved successfully!")
    
    def complete_todo(self):
        """Mark the selected todo as completed"""
        selection = self.todo_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a todo to complete.")
            return
        
        todo_id = int(self.todo_tree.item(selection[0])["values"][0])
        if self.todo_list.complete_todo(todo_id):
            self.load_todos()
            messagebox.showinfo("Success", "Todo marked as completed!")
        else:
            messagebox.showerror("Error", "Failed to complete todo.")
    
    def delete_todo(self):
        """Delete the selected todo"""
        selection = self.todo_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a todo to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this todo?"):
            todo_id = int(self.todo_tree.item(selection[0])["values"][0])
            if self.todo_list.delete_todo(todo_id):
                self.load_todos()
                self.new_todo()
                messagebox.showinfo("Success", "Todo deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete todo.")
    
    def on_select_todo(self, event):
        """Handle todo selection"""
        selection = self.todo_tree.selection()
        if not selection:
            return
        
        todo_id = int(self.todo_tree.item(selection[0])["values"][0])
        todos = self.todo_list.get_todos()
        
        for todo in todos:
            if todo["id"] == todo_id:
                self.title_var.set(todo["title"])
                self.description_text.delete("1.0", tk.END)
                self.description_text.insert("1.0", todo["description"])
                self.due_date_var.set(todo["due_date"] or "")
                self.priority_var.set(todo["priority"])
                self.category_var.set(todo["category"])
                break

def main():
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
