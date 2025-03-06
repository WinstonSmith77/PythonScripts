from pathlib import Path
import datetime

def find_files_in_date_range(folder_path, time_spans, contains=None):
    files_in_range = []

    for timespan in time_spans:

        start_datetime = datetime.datetime.strptime(timespan[0], '%Y-%m-%d %H:%M')
        end_datetime = datetime.datetime.strptime(timespan[1], '%Y-%m-%d %H:%M')
    
        for path in Path(folder_path).rglob('*'):
            if path.is_file():
                if contains is not None and contains in str(path):
                    file_modification_time = datetime.datetime.fromtimestamp(path.stat().st_mtime)
                    if start_datetime <= file_modification_time <= end_datetime:
                        files_in_range.append((str(path), str(file_modification_time)))
                

 
    return files_in_range

# Example usage
folder_path = r'C:/Users/henning/OneDrive/bilder/_lightroom/2025'
start_date = '2025-03-02 15:00'
end_date = '2025-03-02 18:00'
start_date2 = '2025-03-01 15:00'
end_date2 = '2025-03-01 18:00'
start_date3 = '2025-02-28 15:00'
end_date3 = '2025-02-28 18:00'
time_sapns = [(start_date, end_date, start_date2, end_date2, start_date3, end_date3)]
files = find_files_in_date_range(folder_path, time_sapns, "RW2")
for file in files:
    print(file)
