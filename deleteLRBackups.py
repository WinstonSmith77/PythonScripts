import subprocess
import os

pathToExe = "C:/Program Files/Adobe/Adobe Lightroom Classic/lightroom.exe"
backupFolder = "C:/Users/matze/OneDrive/lightroom backup"

def delete_old_backups():
    backups = os.listdir(backupFolder)
    print(backups)

def start_Exe():
    subprocess.run(pathToExe)

if __name__ == "__main__":
      delete_old_backups()
      #start_Exe()  