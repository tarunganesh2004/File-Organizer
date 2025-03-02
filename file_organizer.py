import os
import shutil
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_DIR = "C:\Users\emada\Downloads\File-Organizer"  # Change to your folder
SORT_DIR = "C:\Users\emada\Downloads\test"  # Destination folder
LOG_FILE = "logs.txt"
UNDO_FILE = "config.json"

# File Categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Archives": [".zip", ".rar", ".7z", ".tar.gz"],
    "Music": [".mp3", ".wav", ".flac"],
    "Others": [],
}


# Load undo history
def load_undo():
    if os.path.exists(UNDO_FILE):
        with open(UNDO_FILE, "r") as file:
            return json.load(file)
    return {}


# Save undo history
def save_undo(data):
    with open(UNDO_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Logging function
def log_action(action):
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.ctime()}: {action}\n")


# Sorting logic
def sort_files():
    undo_data = {}

    for filename in os.listdir(WATCH_DIR):
        file_path = os.path.join(WATCH_DIR, filename)
        if not os.path.isfile(file_path):
            continue

        file_ext = os.path.splitext(filename)[1].lower()
        category = next(
            (key for key, exts in FILE_TYPES.items() if file_ext in exts), "Others"
        )

        target_folder = os.path.join(SORT_DIR, category)
        os.makedirs(target_folder, exist_ok=True)

        new_path = os.path.join(target_folder, filename)
        shutil.move(file_path, new_path)
        undo_data[new_path] = file_path
        log_action(f"Moved: {file_path} -> {new_path}")

    save_undo(undo_data)
    print("Sorting complete!")


# Undo last operation
def undo_last():
    undo_data = load_undo()
    for new_path, old_path in undo_data.items():
        if os.path.exists(new_path):
            shutil.move(new_path, old_path)
            log_action(f"Restored: {new_path} -> {old_path}")
    save_undo({})
    print("Undo completed!")


# Real-time monitoring class
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Detected new file: {event.src_path}, sorting now...")
            sort_files()


# Start monitoring
def monitor_folder():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"Monitoring {WATCH_DIR} for new files...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    print("1. Sort files now\n2. Monitor folder for changes\n3. Undo last operation")
    choice = input("Choose an option: ")

    if choice == "1":
        sort_files()
    elif choice == "2":
        monitor_folder()
    elif choice == "3":
        undo_last()
    else:
        print("Invalid choice!")
