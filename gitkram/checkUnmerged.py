import git
import argparse

def get_conflicted_files(repo):
    """
    Returns a list of conflicted files in the repository.
    """
    def is_unmerged(diff):
         return 'u' in diff.change_type.lower()
    conflicted_files=[diff.a_path for diff in repo.index.diff(None) if is_unmerged(diff)]
       
    return conflicted_files

if __name__ == "__main__":
    # Replace with the path to your Git repository
 
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
