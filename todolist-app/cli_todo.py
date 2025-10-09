import json
import os
from datetime import datetime, date

class TodoList:
    def __init__(self):
        self.todo_file = "todos.json"
        self.load_todos()

    def load_todos(self):
        """Load existing todos from file"""
        if os.path.exists(self.todo_file):
            try:
                with open(self.todo_file, "r") as f:
                    self.todos = json.load(f)
            except json.JSONDecodeError:
                self.todos = []
        else:
            self.todos = []

    def save_todos(self):
        """Save todos to file"""
        with open(self.todo_file, "w") as f:
            json.dump(self.todos, f, indent=4)

    def add_todo(self, title, description="", due_date=None, priority="medium", category="general"):
        """Add a new todo item"""
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "description": description,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "completed": False,
            "completed_date": None
        }
        self.todos.append(todo)
        self.save_todos()
        return todo["id"]

    def complete_todo(self, todo_id):
        """Mark a todo as completed"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                todo["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_todos()
                return True
        return False

    def delete_todo(self, todo_id):
        """Delete a todo item"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                self.todos.remove(todo)
                self.save_todos()
                return True
        return False

    def get_todos(self, filter_completed=None, category=None, priority=None):
        """Get filtered todos"""
        filtered_todos = self.todos
        
        if filter_completed is not None:
            filtered_todos = [t for t in filtered_todos if t["completed"] == filter_completed]
            
        if category:
            filtered_todos = [t for t in filtered_todos if t["category"].lower() == category.lower()]
            
        if priority:
            filtered_todos = [t for t in filtered_todos if t["priority"].lower() == priority.lower()]
            
        return filtered_todos

    def get_categories(self):
        """Get list of all categories"""
        return sorted(set(todo["category"] for todo in self.todos))

    def update_todo(self, todo_id, title=None, description=None, due_date=None, 
                   priority=None, category=None):
        """Update a todo item"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                if title is not None:
                    todo["title"] = title
                if description is not None:
                    todo["description"] = description
                if due_date is not None:
                    todo["due_date"] = due_date
                if priority is not None:
                    todo["priority"] = priority
                if category is not None:
                    todo["category"] = category
                self.save_todos()
                return True
        return False

def print_todo(todo):
    """Print a todo item in a formatted way"""
    status = "" if todo["completed"] else " "
    print(f"\n[{status}] #{todo['id']} - {todo['title']}")
    if todo["description"]:
        print(f"Description: {todo['description']}")
    print(f"Category: {todo['category']}")
    print(f"Priority: {todo['priority']}")
    if todo["due_date"]:
        print(f"Due Date: {todo['due_date']}")
    print(f"Created: {todo['created_date']}")
    if todo["completed"]:
        print(f"Completed: {todo['completed_date']}")
    print("-" * 50)

def main():
    todo_list = TodoList()
    
    while True:
        print("\nTodo List Manager")
        print("1. Add Todo")
        print("2. List Todos")
        print("3. Complete Todo")
        print("4. Update Todo")
        print("5. Delete Todo")
        print("6. Filter Todos")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            title = input("Enter todo title: ")
            description = input("Enter description (optional): ")
            due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ")
            if due_date and not due_date.strip():
                due_date = None
            
            print("\nPriority levels: low, medium, high")
            priority = input("Enter priority (default: medium): ").lower() or "medium"
            
            categories = todo_list.get_categories()
            if categories:
                print("\nExisting categories:", ", ".join(categories))
            category = input("Enter category (default: general): ").lower() or "general"
            
            todo_id = todo_list.add_todo(title, description, due_date, priority, category)
            print(f"\nTodo added successfully with ID: {todo_id}")

        elif choice == "2":
            todos = todo_list.get_todos()
            if not todos:
                print("No todos found.")
                continue
                
            print("\nYour Todos:")
            for todo in todos:
                print_todo(todo)

        elif choice == "3":
            todos = todo_list.get_todos(filter_completed=False)
            if not todos:
                print("No incomplete todos found.")
                continue
                
            print("\nIncomplete Todos:")
            for todo in todos:
                print_todo(todo)
                
            try:
                todo_id = int(input("\nEnter todo ID to complete (0 to cancel): "))
                if todo_id == 0:
                    continue
                if todo_list.complete_todo(todo_id):
                    print("Todo marked as completed!")
                else:
                    print("Todo not found.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "4":
            todos = todo_list.get_todos()
            if not todos:
                print("No todos found.")
                continue
                
            print("\nYour Todos:")
            for todo in todos:
                print_todo(todo)
                
            try:
                todo_id = int(input("\nEnter todo ID to update (0 to cancel): "))
                if todo_id == 0:
                    continue
                    
                title = input("Enter new title (press Enter to skip): ")
                description = input("Enter new description (press Enter to skip): ")
                due_date = input("Enter new due date (YYYY-MM-DD) (press Enter to skip): ")
                priority = input("Enter new priority (low/medium/high) (press Enter to skip): ")
                category = input("Enter new category (press Enter to skip): ")
                
                updates = {}
                if title.strip():
                    updates["title"] = title
                if description.strip():
                    updates["description"] = description
                if due_date.strip():
                    updates["due_date"] = due_date
                if priority.strip():
                    updates["priority"] = priority.lower()
                if category.strip():
                    updates["category"] = category.lower()
                
                if todo_list.update_todo(todo_id, **updates):
                    print("Todo updated successfully!")
                else:
                    print("Todo not found.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "5":
            todos = todo_list.get_todos()
            if not todos:
                print("No todos found.")
                continue
                
            print("\nYour Todos:")
            for todo in todos:
                print_todo(todo)
                
            try:
                todo_id = int(input("\nEnter todo ID to delete (0 to cancel): "))
                if todo_id == 0:
                    continue
                if todo_list.delete_todo(todo_id):
                    print("Todo deleted successfully!")
                else:
                    print("Todo not found.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "6":
            print("\nFilter Options:")
            print("1. By Status")
            print("2. By Category")
            print("3. By Priority")
            
            filter_choice = input("\nEnter filter choice (1-3): ")
            
            if filter_choice == "1":
                status_choice = input("Show completed todos? (y/n): ").lower()
                filter_completed = status_choice == 'y'
                todos = todo_list.get_todos(filter_completed=filter_completed)
            
            elif filter_choice == "2":
                categories = todo_list.get_categories()
                if not categories:
                    print("No categories found.")
                    continue
                print("\nCategories:", ", ".join(categories))
                category = input("Enter category to filter by: ").lower()
                todos = todo_list.get_todos(category=category)
            
            elif filter_choice == "3":
                print("\nPriority levels: low, medium, high")
                priority = input("Enter priority to filter by: ").lower()
                todos = todo_list.get_todos(priority=priority)
            
            else:
                print("Invalid filter choice.")
                continue
            
            if not todos:
                print("No matching todos found.")
                continue
                
            print("\nFiltered Todos:")
            for todo in todos:
                print_todo(todo)

        elif choice == "7":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
