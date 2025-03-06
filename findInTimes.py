from pathlib import Path
from datetime import datetime, timedelta

def find_files_in_date_range(folder_path, time_spans, contains=None):
    files_in_range = []

    for timespan in time_spans:

        start_datetime = timespan[0]
        end_datetime = timespan[1]
    
        for path in Path(folder_path).rglob('*'):
            if path.is_file():
                if contains is not None and contains in str(path):
                    file_modification_time = datetime.fromtimestamp(path.stat().st_mtime)
                    if start_datetime <= file_modification_time <= end_datetime:
                        files_in_range.append((path, str(file_modification_time)))
                

 
    return files_in_range

# Example usage
folder_path = r'C:/Users/henning/OneDrive/bilder/_lightroom/2025'
start_date = datetime(2025,2,27, 15)
end_date = datetime(2025,2,27, 20)


timespans = [(start_date + timedelta(days=i), end_date + timedelta(days=i)) for i in range(0, 7)]

files = find_files_in_date_range(folder_path, timespans, "RW2")
for file in files:
    print(file)
