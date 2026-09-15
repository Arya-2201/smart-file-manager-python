from pathlib import Path
folder = Path(".")
print("Items inside this folder:")
for item in folder.iterdir():
    print(item)
    