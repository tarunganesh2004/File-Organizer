# 📂 File Organizer Script

A fully-featured Python script to **automatically organize files** into categorized folders. It includes:

✅ **Sorting by File Type** (Images, Videos, Documents, etc.)  
✅ **Live Monitoring** (Auto-sort new files)  
✅ **Undo Last Sorting Operation** (Restore files to original location)  
✅ **Logging & Reports** (Track every move)  
✅ **Cross-Platform Compatibility** (Windows, Mac, Linux)

---

## 🚀 Features

- **Sort Files Manually:** Organizes files in the specified folder.
- **Real-Time Monitoring:** Watches a directory for new files and auto-sorts them.
- **Undo Last Sorting:** Moves files back to their original locations.
- **Logs Every Action:** Keeps a record of all file movements.

---

## 🛠️ Requirements

Ensure you have Python **3.7+** installed and the required dependencies:

```sh
pip install watchdog
```

---

## 📦 Installation & Usage

### 1️⃣ **Download the Script**
Clone this repository or download the script manually.

```sh
git clone https://github.com/tarunganesh2004/File-Organizer.git
cd File-Organizer
```

### 2️⃣ **Modify Configuration**
Edit the script to update these paths:

```python
WATCH_DIR = r"C:\Users\YourUsername\Downloads"  # Folder to monitor
SORT_DIR = r"C:\Users\YourUsername\SortedFiles"  # Destination folder
```

### 3️⃣ **Run the Script**
Execute the script and choose an option:

```sh
python file_organizer.py
```

#### 🏷️ Options:
1️⃣ **Sort files now** (Manually organize all files in the folder)  
2️⃣ **Monitor folder for changes** (Automatically sort new files)  
3️⃣ **Undo last operation** (Restore previous file locations)

---

## 📂 Folder Structure

```
📁 file-organizer/
 ├── file_organizer.py   # Main script
 ├── config.json         # Stores undo data
 ├── logs.txt            # Logs all file movements
 ├── README.md           # Documentation
```

---

## 🔄 How It Works

### ✅ Sorting Logic:
- The script scans `WATCH_DIR` for files.
- It **categorizes files** based on extensions (e.g., `.jpg` → Images, `.mp4` → Videos).
- Moves each file into the respective folder inside `SORT_DIR`.

### 🔎 Real-Time Monitoring:
- Uses `watchdog` to detect new files.
- Auto-sorts any newly added files.

### 🔙 Undo Last Operation:
- Saves previous locations in `config.json`.
- Moves files back to their original locations when undo is triggered.

---

## 📜 File Categories

| Category   | Extensions |
|------------|--------------------------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp |
| **Videos** | .mp4, .mkv, .mov, .avi |
| **Documents** | .pdf, .docx, .xlsx, .pptx, .txt |
| **Archives** | .zip, .rar, .7z, .tar.gz |
| **Music** | .mp3, .wav, .flac |
| **Others** | Any unclassified files |

---

## 🛠️ Troubleshooting

### 🔥 Common Issues & Fixes
1. **Script doesn't run?** Ensure you have **Python 3.7+** installed.
2. **watchdog module not found?** Install it via `pip install watchdog`.
3. **Files not moving?** Check if paths are correct in `WATCH_DIR` and `SORT_DIR`.


---

## ⭐ Like This Project?
Give it a ⭐ on GitHub! Contributions are welcome. 🙌
