import git

def is_file_unmerged(repo, filename):
    """
    Checks if a file is unmerged (has conflicts) in the current commit.
    """
    try:
        repo.git.checkout('HEAD', '--', filename)
        return False
    except git.exc.GitCommandError:
        return True

def get_unmerged_files(repo):
    """
    Returns a list of unmerged files in the repository.
    """
    unmerged_files = []
    for diff in repo.index.diff(None):
        if is_file_unmerged(repo, diff.a_path):
            unmerged_files.append(diff.a_path)
    return unmerged_files

if __name__ == "__main__":
    # Replace with the path to your Git repository
    repo_path = "/path/to/your/git/repo"
    repo = git.Repo(repo_path)

    unmerged_files = get_unmerged_files(repo)
    if unmerged_files:
        print("Unmerged files:")
        for filename in unmerged_files:
            print(filename)
    else:
        print("No unmerged files found.")
