import os

def path_length(path):
    """Calculate the length of a file path string."""
    return len(path)

def path_depth(path):
    """Calculate the depth of a path (number of directories)."""
    return len(os.path.normpath(path).split(os.sep))

def find_longest_path(root_folder):
    """Find the longest path in a folder recursively."""
    longest_path = ""
    max_length = 0
    
    for root, dirs, files in os.walk(root_folder):
        # Check directory paths
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if len(dir_path) > max_length:
                max_length = len(dir_path)
                longest_path = dir_path
        
        # Check file paths
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if len(file_path) > max_length:
                max_length = len(file_path)
                longest_path = file_path
    
    return longest_path, max_length

# Example usage
if __name__ == "__main__":
    sample_path = r"C:\Users\henning\source\easymapGit\dev"
    print(f"Path: {sample_path}")
    print(f"Length: {path_length(sample_path)} characters")
    print(f"Depth: {path_depth(sample_path)} levels")
    
    # Find longest path
    longest, length = find_longest_path(sample_path)
    print(f"\nLongest path: {longest}")
    print(f"Length: {length} characters")