import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
from cli_diary import PersonalDiary

class DiaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary")
        self.root.geometry("800x600")
        
        # Initialize diary
        self.diary = PersonalDiary()
        
        # Create GUI elements
        self.setup_gui()
        
        # Load entries
        self.load_entries_list()
        
    def setup_gui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left side - Entries list
        self.entries_frame = ttk.LabelFrame(self.main_frame, text="Entries", padding="5")
        self.entries_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Entries listbox
        self.entries_listbox = tk.Listbox(self.entries_frame, width=40)
        self.entries_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.entries_listbox.bind("<<ListboxSelect>>", self.on_select_entry)
        
        # Scrollbar for entries
        entries_scrollbar = ttk.Scrollbar(self.entries_frame, orient=tk.VERTICAL, 
                                        command=self.entries_listbox.yview)
        entries_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.entries_listbox["yscrollcommand"] = entries_scrollbar.set
        
        # Right side - Entry view/edit
        self.entry_frame = ttk.LabelFrame(self.main_frame, text="Entry", padding="5")
        self.entry_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Title
        ttk.Label(self.entry_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.entry_frame, textvariable=self.title_var)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Content
        ttk.Label(self.entry_frame, text="Content:").grid(row=1, column=0, sticky=tk.W)
        self.content_text = scrolledtext.ScrolledText(self.entry_frame, width=40, height=20)
        self.content_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons
        button_frame = ttk.Frame(self.entry_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="New Entry", command=self.new_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Entry", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Entry", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.entries_frame.rowconfigure(0, weight=1)
        self.entry_frame.columnconfigure(1, weight=1)
        self.entry_frame.rowconfigure(2, weight=1)
        
    def load_entries_list(self):
        self.entries_listbox.delete(0, tk.END)
        entries = self.diary.list_entries()
        self.timestamps = []
        
        for timestamp in sorted(entries.keys(), reverse=True):
            entry = entries[timestamp]
            self.entries_listbox.insert(tk.END, f"{timestamp} - {entry['title']}")
            self.timestamps.append(timestamp)
    
    def on_select_entry(self, event):
        selection = self.entries_listbox.curselection()
        if selection:
            index = selection[0]
            timestamp = self.timestamps[index]
            entry = self.diary.view_entry(timestamp)
            if entry:
                self.title_var.set(entry["title"])
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", entry["content"])
    
    def new_entry(self):
        self.title_var.set("")
        self.content_text.delete("1.0", tk.END)
        self.entries_listbox.selection_clear(0, tk.END)
    
    def save_entry(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        
        if not title or not content:
            messagebox.showwarning("Warning", "Please enter both title and content.")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.diary.add_entry(title, content)
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

def main():
    root = tk.Tk()
    app = DiaryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
