from model import FileInfo

def search_files(files, keyword):
    result = []

    keyword = keyword.lower()

    for file in files:
        if keyword in file.name.lower():
            result.append(file)

    return result
