from pathlib import Path
import datetime

def find_files_in_date_range(folder_path, start_date, end_date, contains=None):
    files_in_range = []
    start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M')
    end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M')

   
    for path in Path(folder_path).rglob('*'):
        if path.is_file():
            if contains is not None and contains in str(path):
                file_modification_time = datetime.datetime.fromtimestamp(path.stat().st_mtime)
                if start_datetime <= file_modification_time <= end_datetime:
                    files_in_range.append((str(path), str(file_modification_time)))
                

 
    return files_in_range

# Example usage
folder_path = r'C:/Users/henning/OneDrive/bilder/_lightroom/2025/2025-03-02'
start_date = '2025-03-02 15:00'
end_date = '2025-03-02 22:59'
files = find_files_in_date_range(folder_path, start_date, end_date, "RW2")
for file in files:
    print(file)
