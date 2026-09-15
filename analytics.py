from collections import Counter

def get_analytics(files):
    total_files = len(files)

    total_size = sum(file.size for file in files)

    largest = max(files, key=lambda file: file.size)

    extensions = Counter(
        file.extension.lower() for file in files
    )

    return {
        "total_files": total_files,
        "total_size": total_size,
        "largest": largest,
        "extensions": extensions
    }