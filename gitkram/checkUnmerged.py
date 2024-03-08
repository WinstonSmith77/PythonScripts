import git
import argparse

def get_conflicted_files(repo):
    """
    Returns a list of unmerged files in the repository.
    """
    conflicted_files = []
    def is_unmerged(diff):
         a = bool(diff.a_blob)
         b = bool (diff.b_blob)
         return a != b  or (a and b and diff.a_blob.hexsha != diff.b_blob.hexsha)
    for diff in repo.index.diff(None):
       if is_unmerged(diff):
            conflicted_files.append(diff.a_blob.path)
    return conflicted_files

if __name__ == "__main__":
    # Replace with the path to your Git repository
    path_repo = r'C:\Users\henning\source\easymapGit\dev'
    if not 'path_repo' in locals():
        parser = argparse.ArgumentParser()
        parser.add_argument("path_repo")
        args = parser.parse_args()
        path_repo = args.path_repo

    repo = git.Repo(path_repo)

    conflicted_files = get_conflicted_files(repo)
    if conflicted_files:
        print("Conflicted files:")
        for filename in conflicted_files:
            print(filename)
    else:
        print("No conflicted files found.")
