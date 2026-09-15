from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from scanner import scan_folder
from search import search_files
from sorter import sort_by_name, sort_by_size
from duplicate import find_duplicates
from analytics import get_analytics

# ---------------- Window ----------------
root = tk.Tk()
root.title("Smart File Manager")
root.geometry("1050x650")

# ---------------- Data ----------------
files = scan_folder(Path.home() / "Downloads")
current_files = files.copy()

# ---------------- Functions ----------------

def format_size(size):
    """Convert bytes into KB / MB / GB"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024


def load_table(file_list):
    for row in table.get_children():
        table.delete(row)

    for file in file_list:
        table.insert(
            "",
            "end",
            values=(
                file.name,
                file.extension,
                format_size(file.size)
            )
        )


def show_text(event=None):
    global current_files

    keyword = search_var.get().strip()

    if keyword == "":
        current_files = files.copy()
    else:
        current_files = search_files(files, keyword)

    load_table(current_files)


def sort_name():
    global current_files
    current_files = sort_by_name(current_files)
    load_table(current_files)


def sort_size():
    global current_files
    current_files = sort_by_size(current_files)
    load_table(current_files)


def show_all():
    global current_files
    current_files = files.copy()
    search_var.set("")
    load_table(current_files)


def show_duplicates():
    global current_files

    duplicate_groups = find_duplicates(files)

    current_files = []

    for group in duplicate_groups.values():
        current_files.extend(group)

    load_table(current_files)


def show_analytics():
    stats = get_analytics(files)

    duplicate_groups = find_duplicates(files)
    duplicate_count = sum(len(g) for g in duplicate_groups.values())

    top_types = stats["extensions"].most_common(5)

    text = (
        f"Total Files : {stats['total_files']}\n"
        f"Total Storage : {format_size(stats['total_size'])}\n"
        f"Largest File : {stats['largest'].name}\n"
        f"Size : {format_size(stats['largest'].size)}\n"
        f"Duplicate Files : {duplicate_count}\n\n"
        f"Top File Types\n"
        f"-----------------------\n"
    )

    for ext, count in top_types:
        name = ext if ext else "No Extension"
        text += f"{name} : {count}\n"

    messagebox.showinfo("Storage Analytics", text)


# ---------------- Header ----------------

header = tk.Frame(root, bg="#2563EB", height=55)
header.pack(fill="x")

tk.Label(
    header,
    text="Smart File Manager",
    bg="#2563EB",
    fg="white",
    font=("Arial", 18, "bold")
).pack(pady=12)

# ---------------- Body ----------------

body = tk.Frame(root)
body.pack(fill="both", expand=True)

# ---------------- Sidebar ----------------

sidebar = tk.Frame(body, bg="#E8E1EB", width=180)
sidebar.pack(side="left", fill="y")

tk.Label(
    sidebar,
    text="MENU",
    bg="#E8E1EB",
    font=("Arial", 12, "bold")
).pack(pady=20)

ttk.Button(
    sidebar,
    text="All Files",
    command=show_all
).pack(fill="x", padx=12, pady=5)

ttk.Button(
    sidebar,
    text="Duplicates",
    command=show_duplicates
).pack(fill="x", padx=12, pady=5)

ttk.Button(
    sidebar,
    text="Analytics",
    command=show_analytics
).pack(fill="x", padx=12, pady=5)

# ---------------- Content ----------------

content = tk.Frame(body)
content.pack(side="right", fill="both", expand=True)

# Search Row

top = tk.Frame(content)
top.pack(fill="x", padx=10, pady=10)

search_var = tk.StringVar()

search_entry = ttk.Entry(top, textvariable=search_var)
search_entry.pack(side="left", fill="x", expand=True)

search_entry.bind("<KeyRelease>", show_text)

ttk.Button(
    top,
    text="Search",
    command=show_text
).pack(side="left", padx=8)

# ---------------- Table ----------------

table = ttk.Treeview(
    content,
    columns=("Name", "Extension", "Size"),
    show="headings"
)

table.heading("Name", text="Name ▲", command=sort_name)
table.heading("Extension", text="Type")
table.heading("Size", text="Size ▼", command=sort_size)

table.column("Name", width=520)
table.column("Extension", width=120, anchor="center")
table.column("Size", width=130, anchor="center")

table.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------- Initial Load ----------------

load_table(current_files)

# ---------------- Run ----------------

root.mainloop()