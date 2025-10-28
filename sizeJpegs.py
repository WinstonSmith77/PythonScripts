import os

def sum_jpeg_sizes(folder_path):
    total_size = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
    return total_size

if __name__ == "__main__":
    folder = "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/bilder"  # Change this to your folder path
    total = sum_jpeg_sizes(folder)
    print(f"Total size of all JPEG files: {total/1024/1024:.1f} mb")