import os

def find_empty_folders(path):
    empty_folders = []
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            empty_folders.append(root)
    return empty_folders

# Example usage
path_to_check = '/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/bilder/_lightroom'
empty_folders = find_empty_folders(path_to_check)
for folder in empty_folders:
    os.rmdir(folder)
    print(folder)