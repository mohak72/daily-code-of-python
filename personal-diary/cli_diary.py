import os
import json
from datetime import datetime

class PersonalDiary:
    def __init__(self):
        self.diary_file = "diary_entries.json"
        self.load_entries()

    def load_entries(self):
        """Load existing diary entries from file"""
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, "r") as f:
                    self.entries = json.load(f)
            except json.JSONDecodeError:
                self.entries = {}
        else:
            self.entries = {}

    def save_entries(self):
        """Save diary entries to file"""
        with open(self.diary_file, "w") as f:
            json.dump(self.entries, f, indent=4)

    def add_entry(self, title, content):
        """Add a new diary entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entries[timestamp] = {
            "title": title,
            "content": content
        }
        self.save_entries()
        return timestamp

    def view_entry(self, timestamp):
        """View a specific diary entry"""
        if timestamp in self.entries:
            return self.entries[timestamp]
        return None

    def list_entries(self):
        """List all diary entries"""
        return self.entries

    def delete_entry(self, timestamp):
        """Delete a diary entry"""
        if timestamp in self.entries:
            del self.entries[timestamp]
            self.save_entries()
            return True
        return False

def main():
    diary = PersonalDiary()
    
    while True:
        print("\nPersonal Diary")
        print("1. Add Entry")
        print("2. View Entries")
        print("3. Delete Entry")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            title = input("Enter entry title: ")
            print("Enter your diary entry (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            content = "\n".join(lines)
            timestamp = diary.add_entry(title, content)
            print(f"\nEntry added successfully! Timestamp: {timestamp}")

        elif choice == "2":
            entries = diary.list_entries()
            if not entries:
                print("No entries found.")
                continue
                
            print("\nYour Diary Entries:")
            for timestamp, entry in entries.items():
                print(f"\nDate: {timestamp}")
                print(f"Title: {entry['title']}")
                print("Content:")
                print(entry['content'])
                print("-" * 50)

        elif choice == "3":
            entries = diary.list_entries()
            if not entries:
                print("No entries to delete.")
                continue
                
            print("\nSelect entry to delete:")
            timestamps = list(entries.keys())
            for i, timestamp in enumerate(timestamps, 1):
                print(f"{i}. {timestamp} - {entries[timestamp]['title']}")
                
            try:
                index = int(input("\nEnter entry number to delete (0 to cancel): "))
                if index == 0:
                    continue
                if 1 <= index <= len(timestamps):
                    timestamp = timestamps[index-1]
                    if diary.delete_entry(timestamp):
                        print("Entry deleted successfully!")
                    else:
                        print("Failed to delete entry.")
                else:
                    print("Invalid entry number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
