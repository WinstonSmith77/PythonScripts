import os
import shutil

backupFolder = "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/lightroom_backup_mac"
keepNumberOfBackups = 10

def delete_old_backups(path):
    backups = [(item.path, os.path.getctime(item.path)) for item in os.scandir(path) if item.is_dir()]
    backups.sort(key = lambda item : item[0])

    toDelete = backups[0:-keepNumberOfBackups]
    for item in toDelete:
        print(item)
        shutil.rmtree(str(item[0]))
        



if __name__ == "__main__":
    delete_old_backups(backupFolder)
    #start_Exe()  