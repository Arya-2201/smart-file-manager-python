from model import FileInfo

def sort_by_name(files):
    return sorted(files, key=lambda file: file.name.lower())


def sort_by_size(files):
    return sorted(files, key=lambda file: file.size, reverse=True)


def sort_by_extension(files):
    return sorted(files, key=lambda file: file.extension.lower())