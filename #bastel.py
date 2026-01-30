from pathlib import Path

def is_subpath(child: str | Path, parent: str | Path) -> bool:
    child = Path(child).resolve()
    parent = Path(parent).resolve()
    return child.is_relative_to(parent)

if __name__ == "__main__":
    examples = [
        ("/home/user", "/home/user/a", True),
    ]
    for child, parent, expected in examples:
        result = is_subpath(child, parent)
        print(f"is_subpath({child!r}, {parent!r}) -> {result} (expected {expected})")