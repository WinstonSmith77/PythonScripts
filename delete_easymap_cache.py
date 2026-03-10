import os
import shutil
from pathlib import Path

def delete_easymap_cache():
    # Get the TEMP directory from environment variables
    # We use os.environ to get the path, then wrap it in a Path object
    temp_env = os.environ.get('TEMP')
    if not temp_env:
        print("Error: %TEMP% environment variable not found.")
        return

    temp_path = Path(temp_env)
    
    # Construct the full path using Pathlib's / operator
    # Path: %TEMP%\easymap_12.3.0.0\cache
    cache_path = temp_path / "easymap_12.3.0.0" / "cache"
    
    print(f"Looking for: {cache_path}")

    if cache_path.exists():
        try:
            # shutil.rmtree is the most robust way to delete a non-empty directory tree
            # It accepts Path objects directly
            shutil.rmtree(cache_path)
            print(f"Successfully deleted: {cache_path}")
        except Exception as e:
            print(f"Failed to delete {cache_path}. Reason: {e}")
    else:
        print("Directory does not exist.")

if __name__ == "__main__":
    delete_easymap_cache()
