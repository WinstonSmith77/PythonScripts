import json
from pathlib import Path
from typing import Any, List, Tuple


class JsonComparator:
    def __init__(self, *, strict_types: bool = True) -> None:
        self.strict_types = strict_types

    def compare_files(self, left_path: Path, right_path: Path) -> List[dict]:
        left = self._load(left_path)
        right = self._load(right_path)
        return self.compare(left, right)

    def compare(self, left: Any, right: Any) -> List[dict]:
        differences: List[dict] = []
        self._visit(left, right, tuple(), differences)
        return differences

    @staticmethod
    def _load(path: Path) -> Any:
        text = Path(path).read_text(encoding="utf-8")
        return json.loads(text)

    def _visit(self, left: Any, right: Any, path: Tuple[Any, ...], differences: List[dict]) -> None:
        if left == right:
            return

        if self.strict_types and type(left) is not type(right):
            differences.append(self._difference(path, left, right, "Type mismatch"))
            return

        if isinstance(left, dict) and isinstance(right, dict):
            left_keys = set(left.keys())
            right_keys = set(right.keys())
            for key in sorted(left_keys | right_keys):
                step_path = path + (key,)
                if key not in left:
                    differences.append(self._difference(step_path, None, right[key], "Missing on left"))
                elif key not in right:
                    differences.append(self._difference(step_path, left[key], None, "Missing on right"))
                else:
                    self._visit(left[key], right[key], step_path, differences)
            return

        if isinstance(left, list) and isinstance(right, list):
            min_length = min(len(left), len(right))
            for index in range(min_length):
                self._visit(left[index], right[index], path + (index,), differences)
            for index in range(min_length, len(left)):
                differences.append(self._difference(path + (index,), left[index], None, "Extra element on left"))
            for index in range(min_length, len(right)):
                differences.append(self._difference(path + (index,), None, right[index], "Extra element on right"))
            return

        differences.append(self._difference(path, left, right, "Value mismatch"))

    def _difference(self, path: Tuple[Any, ...], left: Any, right: Any, message: str) -> dict:
        return {
            "path": self._format_path(path),
            "left": left,
            "right": right,
            "message": message,
        }

    @staticmethod
    def _format_path(path: Tuple[Any, ...]) -> str:
        if not path:
            return "<root>"
        return " / ".join(str(item) for item in path)


if __name__ == "__main__":
    comparator = JsonComparator()
    style_folder = Path(__file__).parent
    left_file = style_folder / "1.json"
    right_file = style_folder / "2.json"

    if left_file.exists() and right_file.exists():
        diff = comparator.compare_files(left_file, right_file)
        if diff:
            print(f"Found {len(diff)} difference(s):")
            for entry in diff:
                path = entry["path"]
                message = entry["message"]
                left_value = entry["left"]
                right_value = entry["right"]
                print(f"- {path}: {message} (left={left_value!r}, right={right_value!r})")
        else:
            print("No differences found.")
    else:
        print("Place 1.json and 2.json in this folder to compare.")