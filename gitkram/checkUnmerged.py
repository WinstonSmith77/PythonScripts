import git
import argparse


def is_file_conflicted(repo, filename):
    """
    Checks if a file is unmerged (has conflicts) in the current commit.
    """
    try:
        repo.git.checkout('HEAD', '--', filename)
        return False
    except git.exc.GitCommandError:
        return True

def get_conflicted_files(repo):
    """
    Returns a list of unmerged files in the repository.
    """
    conflicted_files = []
    for diff in repo.index.diff(None):
       if diff.a_blob and diff.b_blob and diff.a_blob.hexsha != diff.b_blob.hexsha:
            conflicted_files.append(diff.a_blob.path)
    return conflicted_files

if __name__ == "__main__":
    # Replace with the path to your Git repository
    parser = argparse.ArgumentParser()
    parser.add_argument("path_repo")
    args = parser.parse_args()
    path_repo = args.path_repo

    repo = git.Repo(path_repo)

    conflicted_files = get_conflicted_files(repo)
    if conflicted_files:
        print("Unmerged files:")
        for filename in conflicted_files:
            print(filename)
    else:
        print("No unmerged files found.")
