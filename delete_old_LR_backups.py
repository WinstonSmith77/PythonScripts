import os
import shutil
from pathlib import Path


mac_base_path = Path('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal')

backupFolders = [mac_base_path  /"lightroom_backup_mac", mac_base_path / 'lightroom backup']
keepNumberOfBackups = 5

def delete_old_backups(path):
    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        return
    backups = [(item.path, os.path.getctime(item.path)) for item in os.scandir(path) if item.is_dir()]
    backups.sort(key = lambda item : item[0])

    toDelete = backups[0:-keepNumberOfBackups]
    for item in toDelete:
        pathToDelete = item[0]
        print(f"Deleting {pathToDelete}")
        shutil.rmtree(pathToDelete)
        
if __name__ == "__main__":
    for backupFolder in backupFolders:
        delete_old_backups(backupFolder)
      