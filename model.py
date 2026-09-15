from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileInfo:
    name: str
    path: Path
    size: int
    extension: str