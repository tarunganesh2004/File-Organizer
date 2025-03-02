import os
import shutil
import json
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Default Configurations
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {"watch_dir": "", "sort_dir": ""}


# Load Configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return DEFAULT_CONFIG


# Save Configuration
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


# File Categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Archives": [".zip", ".rar", ".7z", ".tar.gz"],
    "Music": [".mp3", ".wav", ".flac"],
    "Others": [],
}

config = load_config()


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("400x300")

        # Folder Selection
        tk.Label(root, text="Watch Folder:").pack()
        self.watch_dir_entry = tk.Entry(root, width=40)
        self.watch_dir_entry.pack()
        self.watch_dir_entry.insert(0, config["watch_dir"])
        tk.Button(root, text="Browse", command=self.select_watch_folder).pack()

        tk.Label(root, text="Sort Folder:").pack()
        self.sort_dir_entry = tk.Entry(root, width=40)
        self.sort_dir_entry.pack()
        self.sort_dir_entry.insert(0, config["sort_dir"])
        tk.Button(root, text="Browse", command=self.select_sort_folder).pack()

        # Buttons
        tk.Button(root, text="Sort Files Now", command=self.sort_files).pack(pady=5)
        tk.Button(root, text="Start Monitoring", command=self.start_monitoring).pack(
            pady=5
        )
        tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring).pack(
            pady=5
        )
        tk.Button(root, text="Undo Last Sort", command=self.undo_last).pack(pady=5)

        # Status Log
        self.status_label = tk.Label(root, text="Status: Ready", fg="green")
        self.status_label.pack()

        self.observer = None

    def select_watch_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.watch_dir_entry.delete(0, tk.END)
            self.watch_dir_entry.insert(0, folder)
            config["watch_dir"] = folder
            save_config(config)

    def select_sort_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sort_dir_entry.delete(0, tk.END)
            self.sort_dir_entry.insert(0, folder)
            config["sort_dir"] = folder
            save_config(config)

    def sort_files(self):
        watch_dir = self.watch_dir_entry.get()
        sort_dir = self.sort_dir_entry.get()

        if not os.path.exists(watch_dir) or not os.path.exists(sort_dir):
            messagebox.showerror("Error", "Invalid directories!")
            return

        undo_data = {}
        for filename in os.listdir(watch_dir):
            file_path = os.path.join(watch_dir, filename)
            if not os.path.isfile(file_path):
                continue

            file_ext = os.path.splitext(filename)[1].lower()
            category = next(
                (key for key, exts in FILE_TYPES.items() if file_ext in exts), "Others"
            )

            target_folder = os.path.join(sort_dir, category)
            os.makedirs(target_folder, exist_ok=True)

            new_path = os.path.join(target_folder, filename)
            shutil.move(file_path, new_path)
            undo_data[new_path] = file_path

        save_config({"undo": undo_data})
        self.status_label.config(text="Status: Files Sorted", fg="blue")
        messagebox.showinfo("Success", "Files sorted successfully!")

    def start_monitoring(self):
        if self.observer:
            return

        watch_dir = self.watch_dir_entry.get()
        if not os.path.exists(watch_dir):
            messagebox.showerror("Error", "Invalid watch directory!")
            return

        self.observer = Observer()
        event_handler = FileHandler(self)
        self.observer.schedule(event_handler, watch_dir, recursive=False)
        self.observer.start()
        self.status_label.config(text="Status: Monitoring...", fg="orange")
        threading.Thread(target=self.run_observer, daemon=True).start()

    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer = None
            self.status_label.config(text="Status: Monitoring Stopped", fg="red")

    def run_observer(self):
        try:
            self.observer.join()
        except Exception:
            pass

    def undo_last(self):
        undo_data = load_config().get("undo", {})
        for new_path, old_path in undo_data.items():
            if os.path.exists(new_path):
                shutil.move(new_path, old_path)
        save_config({"undo": {}})
        self.status_label.config(text="Status: Undo Complete", fg="green")
        messagebox.showinfo("Undo", "Files restored to original locations!")


class FileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        if not event.is_directory:
            self.app.sort_files()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
