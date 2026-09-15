from pathlib import Path
from scanner import scan_folder
from duplicate import find_duplicates

# Build the file database
files = scan_folder(Path.home() / "Downloads")

# Find duplicate files
duplicates = find_duplicates(files)

print("\nDuplicate Files\n")

for hash_value, group in duplicates.items():
    print("-" * 30)
    for file in group:
        print(file.path)