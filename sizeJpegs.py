import os
from PIL import Image
from PIL.ExifTags import TAGS

def get_creation_date(file_path):
   # print(f"Getting creation date for: {file_path}")
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id)
               # print(f"Tag: {tag}, Value: {value}")
                if tag == 'DateTimeOriginal' or tag == 'DateTime':
                    print(f"Found creation date: {value} {tag}")
                    return value
    except Exception:
        pass
    return None

def sum_jpeg_sizes(folder_path):
    total_size = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
                creation_date = get_creation_date(file_path)
                
               # print(f"{file}: Creation date: {creation_date}")
    return total_size

if __name__ == "__main__":
    folder = "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/bilder"
    total = sum_jpeg_sizes(folder)
    print(f"Total size of all JPEG files: {total/1024/1024/1024:.2f} GB")