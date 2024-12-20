import subprocess
import os

import send2trash

pathToExe = "C:/Program Files/Adobe/Adobe Lightroom Classic/lightroom.exe"
backupFolder = "C:/Users/matze/OneDrive/lightroom backup"
keepNumberOfBackups = 10

def delete_old_backups():
    backups = [(item.path, os.path.getctime(item.path)) for item in os.scandir(backupFolder) if item.is_dir()]
    backups.sort(key = lambda item : item[0])

    toDelete = backups[0:-keepNumberOfBackups]
    for item in toDelete:
        print(item)
        send2trash.send2trash(item[0].replace('/', "\\"))

def start_Exe():
    subprocess.call(pathToExe)

if __name__ == "__main__":
    delete_old_backups()
    #start_Exe()  