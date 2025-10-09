import os
import json
from datetime import datetime
import base64
import csv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PersonalDiary:
    def __init__(self):
        self.diary_file = "diary_entries.json"
        self.password = None
        self.fernet = None
        self.setup_encryption()
        self.load_entries()

    def setup_encryption(self):
        """Initialize encryption with password"""
        if not self.password:
            self.password = input("Enter your diary password (remember this!): ").encode()
        
        # Generate key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"diary_salt",  # In production, use a random salt and store it
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        self.fernet = Fernet(key)

    def encrypt_data(self, data):
        """Encrypt string data"""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        """Decrypt string data"""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return encrypted_data  # Return as is if not encrypted

    def load_entries(self):
        """Load existing diary entries from file"""
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, "r") as f:
                    encrypted_data = json.load(f)
                    # Decrypt entries
                    self.entries = {}
                    for timestamp, entry in encrypted_data.items():
                        self.entries[timestamp] = {
                            "title": self.decrypt_data(entry["title"]),
                            "content": self.decrypt_data(entry["content"]),
                            "category": entry.get("category", "General"),
                            "tags": entry.get("tags", []),
                            "mood": entry.get("mood", "neutral")
                        }
            except Exception:
                self.entries = {}
        else:
            self.entries = {}

    def save_entries(self):
        """Save diary entries to file with encryption"""
        encrypted_entries = {}
        for timestamp, entry in self.entries.items():
            encrypted_entries[timestamp] = {
                "title": self.encrypt_data(entry["title"]),
                "content": self.encrypt_data(entry["content"]),
                "category": entry["category"],
                "tags": entry["tags"],
                "mood": entry["mood"]
            }
        with open(self.diary_file, "w") as f:
            json.dump(encrypted_entries, f, indent=4)

    def add_entry(self, title, content, category="General", tags=None, mood="neutral"):
        """Add a new diary entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entries[timestamp] = {
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "mood": mood
        }
        self.save_entries()
        return timestamp

    def search_entries(self, query):
        """Search entries by title, content, category, or tags"""
        results = {}
        query = query.lower()
        for timestamp, entry in self.entries.items():
            if (query in entry["title"].lower() or
                query in entry["content"].lower() or
                query in entry["category"].lower() or
                query in [tag.lower() for tag in entry["tags"]]):
                results[timestamp] = entry
        return results

    def get_categories(self):
        """Get list of all categories"""
        return sorted(set(entry["category"] for entry in self.entries.values()))

    def get_all_tags(self):
        """Get list of all unique tags"""
        tags = set()
        for entry in self.entries.values():
            tags.update(entry["tags"])
        return sorted(tags)

    def export_to_csv(self, filename):
        """Export entries to CSV file"""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Title", "Content", "Category", "Tags", "Mood"])
            for timestamp, entry in self.entries.items():
                writer.writerow([
                    timestamp,
                    entry["title"],
                    entry["content"],
                    entry["category"],
                    ",".join(entry["tags"]),
                    entry["mood"]
                ])

def main():
    diary = PersonalDiary()
    
    while True:
        print("\nPersonal Diary")
        print("1. Add Entry")
        print("2. View Entries")
        print("3. Search Entries")
        print("4. View by Category")
        print("5. Export to CSV")
        print("6. Delete Entry")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
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
            
            # Get category
            print("\nCategories:", ", ".join(diary.get_categories()) or "No categories yet")
            category = input("Enter category (press Enter for 'General'): ") or "General"
            
            # Get tags
            tags_input = input("Enter tags (comma-separated): ")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            
            # Get mood
            mood = input("Enter mood (happy/sad/neutral): ") or "neutral"
            
            timestamp = diary.add_entry(title, content, category, tags, mood)
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
                print(f"Category: {entry['category']}")
                print(f"Tags: {', '.join(entry['tags']) if entry['tags'] else 'No tags'}")
                print(f"Mood: {entry['mood']}")
                print("Content:")
                print(entry['content'])
                print("-" * 50)

        elif choice == "3":
            query = input("Enter search term: ")
            results = diary.search_entries(query)
            if results:
                print(f"\nFound {len(results)} matching entries:")
                for timestamp, entry in results.items():
                    print(f"\nDate: {timestamp}")
                    print(f"Title: {entry['title']}")
                    print(f"Category: {entry['category']}")
                    print("-" * 30)
            else:
                print("No matching entries found.")

        elif choice == "4":
            categories = diary.get_categories()
            if not categories:
                print("No categories found.")
                continue
                
            print("\nCategories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
                
            try:
                index = int(input("\nSelect category number: ")) - 1
                if 0 <= index < len(categories):
                    category = categories[index]
                    results = diary.search_entries(category)
                    print(f"\nEntries in category '{category}':")
                    for timestamp, entry in results.items():
                        print(f"\nDate: {timestamp}")
                        print(f"Title: {entry['title']}")
                        print("-" * 30)
                else:
                    print("Invalid category number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "5":
            filename = input("Enter export filename (e.g., diary_export.csv): ")
            diary.export_to_csv(filename)
            print(f"Entries exported to {filename}")

        elif choice == "6":
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

        elif choice == "7":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
