from pathlib import Path
from model import FileInfo

def scan_folder(folder: Path):
    files = []

    for item in folder.iterdir():

        if item.is_file():
            files.append(
                FileInfo(
                    name=item.name,
                    path=item,
                    size=item.stat().st_size,
                    extension=item.suffix
                )
            )

        elif item.is_dir():
            files.extend(scan_folder(item))

    return files