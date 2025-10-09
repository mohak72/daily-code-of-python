import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
from datetime import datetime
from cli_diary import PersonalDiary
from ttkthemes import ThemedTk

class DiaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary")
        self.root.geometry("1000x700")
        
        # Theme settings
        self.is_dark_mode = tk.BooleanVar(value=False)
        self.setup_theme()
        
        # Initialize diary
        self.diary = PersonalDiary()
        
        # Create GUI elements
        self.setup_gui()
        
        # Load entries
        self.load_entries_list()
        
    def setup_theme(self):
        """Setup and configure theme"""
        style = ttk.Style()
        self.update_theme()
        
    def update_theme(self):
        """Update theme colors based on mode"""
        style = ttk.Style()
        if self.is_dark_mode.get():
            self.root.configure(bg="#2b2b2b")
            style.configure(".", background="#2b2b2b", foreground="white")
            style.configure("TLabel", background="#2b2b2b", foreground="white")
            style.configure("TFrame", background="#2b2b2b")
            style.configure("TLabelframe", background="#2b2b2b", foreground="white")
            style.configure("TLabelframe.Label", background="#2b2b2b", foreground="white")
            self.entries_listbox.configure(bg="#3b3b3b", fg="white")
            self.content_text.configure(bg="#3b3b3b", fg="white")
            self.search_entry.configure(bg="#3b3b3b", fg="white")
        else:
            self.root.configure(bg="white")
            style.configure(".", background="white", foreground="black")
            style.configure("TLabel", background="white", foreground="black")
            style.configure("TFrame", background="white")
            style.configure("TLabelframe", background="white", foreground="black")
            style.configure("TLabelframe.Label", background="white", foreground="black")
            self.entries_listbox.configure(bg="white", fg="black")
            self.content_text.configure(bg="white", fg="black")
            self.search_entry.configure(bg="white", fg="black")
        
    def setup_gui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Top frame for search and controls
        top_frame = ttk.Frame(self.main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Search
        ttk.Label(top_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(top_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", self.search_entries)
        
        # Dark mode toggle
        ttk.Checkbutton(top_frame, text="Dark Mode", 
                       variable=self.is_dark_mode,
                       command=self.update_theme).pack(side=tk.RIGHT, padx=5)
        
        # Left side - Entries list
        left_frame = ttk.Frame(self.main_frame)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.entries_frame = ttk.LabelFrame(left_frame, text="Entries", padding="5")
        self.entries_frame.pack(fill=tk.BOTH, expand=True)
        
        # Entries listbox
        self.entries_listbox = tk.Listbox(self.entries_frame, width=40)
        self.entries_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entries_listbox.bind("<<ListboxSelect>>", self.on_select_entry)
        
        # Scrollbar for entries
        entries_scrollbar = ttk.Scrollbar(self.entries_frame, orient=tk.VERTICAL, 
                                        command=self.entries_listbox.yview)
        entries_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.entries_listbox["yscrollcommand"] = entries_scrollbar.set
        
        # Category filter
        category_frame = ttk.Frame(left_frame)
        category_frame.pack(fill=tk.X, pady=5)
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var)
        self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.filter_by_category)
        
        # Right side - Entry view/edit
        self.entry_frame = ttk.LabelFrame(self.main_frame, text="Entry", padding="5")
        self.entry_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Title
        title_frame = ttk.Frame(self.entry_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(title_frame, text="Title:").pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, textvariable=self.title_var)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Category and tags
        meta_frame = ttk.Frame(self.entry_frame)
        meta_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(meta_frame, text="Category:").pack(side=tk.LEFT)
        self.entry_category_var = tk.StringVar()
        self.entry_category = ttk.Entry(meta_frame, textvariable=self.entry_category_var)
        self.entry_category.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(meta_frame, text="Tags:").pack(side=tk.LEFT)
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(meta_frame, textvariable=self.tags_var)
        self.tags_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Mood
        mood_frame = ttk.Frame(self.entry_frame)
        mood_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(mood_frame, text="Mood:").pack(side=tk.LEFT)
        self.mood_var = tk.StringVar(value="neutral")
        for mood in ["happy", "neutral", "sad"]:
            ttk.Radiobutton(mood_frame, text=mood.capitalize(), 
                          variable=self.mood_var, 
                          value=mood).pack(side=tk.LEFT, padx=5)
        
        # Content
        ttk.Label(self.entry_frame, text="Content:").grid(row=3, column=0, sticky=tk.W)
        self.content_text = scrolledtext.ScrolledText(self.entry_frame, width=50, height=20)
        self.content_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons
        button_frame = ttk.Frame(self.entry_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="New Entry", 
                  command=self.new_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Entry", 
                  command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Entry", 
                  command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", 
                  command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.entry_frame.columnconfigure(1, weight=1)
        self.entry_frame.rowconfigure(4, weight=1)
        
    def load_entries_list(self):
        self.entries_listbox.delete(0, tk.END)
        entries = self.diary.list_entries()
        self.timestamps = []
        
        # Update category list
        categories = ["All"] + self.diary.get_categories()
        self.category_combo["values"] = categories
        if not self.category_var.get() in categories:
            self.category_var.set("All")
        
        for timestamp in sorted(entries.keys(), reverse=True):
            entry = entries[timestamp]
            if (self.category_var.get() == "All" or 
                entry["category"] == self.category_var.get()):
                self.entries_listbox.insert(tk.END, 
                    f"{timestamp} - {entry['title']} ({entry['category']})")
                self.timestamps.append(timestamp)
    
    def search_entries(self, event=None):
        query = self.search_entry.get().strip()
        if query:
            results = self.diary.search_entries(query)
            self.entries_listbox.delete(0, tk.END)
            self.timestamps = []
            for timestamp in sorted(results.keys(), reverse=True):
                entry = results[timestamp]
                self.entries_listbox.insert(tk.END, 
                    f"{timestamp} - {entry['title']} ({entry['category']})")
                self.timestamps.append(timestamp)
        else:
            self.load_entries_list()
    
    def filter_by_category(self, event=None):
        self.load_entries_list()
    
    def on_select_entry(self, event):
        selection = self.entries_listbox.curselection()
        if selection:
            index = selection[0]
            timestamp = self.timestamps[index]
            entry = self.diary.view_entry(timestamp)
            if entry:
                self.title_var.set(entry["title"])
                self.entry_category_var.set(entry["category"])
                self.tags_var.set(", ".join(entry["tags"]))
                self.mood_var.set(entry.get("mood", "neutral"))
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", entry["content"])
    
    def new_entry(self):
        self.title_var.set("")
        self.entry_category_var.set("General")
        self.tags_var.set("")
        self.mood_var.set("neutral")
        self.content_text.delete("1.0", tk.END)
        self.entries_listbox.selection_clear(0, tk.END)
    
    def save_entry(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        category = self.entry_category_var.get().strip() or "General"
        tags = [tag.strip() for tag in self.tags_var.get().split(",") if tag.strip()]
        mood = self.mood_var.get()
        
        if not title or not content:
            messagebox.showwarning("Warning", "Please enter both title and content.")
            return
        
        self.diary.add_entry(title, content, category, tags, mood)
        self.load_entries_list()
        messagebox.showinfo("Success", "Entry saved successfully!")
    
    def delete_entry(self):
        selection = self.entries_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
            index = selection[0]
            timestamp = self.timestamps[index]
            if self.diary.delete_entry(timestamp):
                self.load_entries_list()
                self.new_entry()
                messagebox.showinfo("Success", "Entry deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete entry.")
    
    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export diary entries"
        )
        if filename:
            try:
                self.diary.export_to_csv(filename)
                messagebox.showinfo("Success", f"Entries exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export entries: {str(e)}")

def main():
    root = ThemedTk(theme="arc")  # You can use other themes like "equilux" for dark mode
    app = DiaryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
