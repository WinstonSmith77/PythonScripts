# Python Coding Guidelines

## General Code Style
- Follow **PEP 8** standards for code formatting.
- Use **4 spaces** for indentation.
- Prefer **snake_case** for variables and functions, and **PascalCase** for classes.
- Sort imports alphabetically within their groups (standard library, third-party, local).

## Type Hinting
- ADD type hints to all function arguments and return values.
- Use built-in collection types (e.g., `list`, `dict`, `tuple`) instead of `typing` aliases where possible (Python 3.9+).
- Use `Optional[T]` or `T | None` for values that can be None.

## File System & Paths
- **ALWAYS** use `pathlib.Path` instead of `os.path` for path manipulations.
- Use the `/` operator for path concatenation (e.g., `folder / "file.txt"`).
- Use `Path.read_text()` and `Path.write_text()` for simple file I/O.

## Error Handling
- Catch **specific exceptions** (e.g., `FileNotFoundError`, `ValueError`) rather than a bare `except:`.
- Use `try/except/else/finally` blocks to handle resources properly.

## String Formatting
- Use **f-strings** (`f"{var}"`) for string interpolation instead of `%` formatting or `.format()`.

## Documentation
- Include docstrings for all modules, classes, and public functions.
- Use clear, descriptive variable names that imply their purpose.

## Project Specifics
- This project uses **Poetry** for dependency management.
- When working with geospatial data, ensure compatibility with existing map rendering logic found in the codebase.
