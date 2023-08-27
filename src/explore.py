import re
from pathlib import Path
from rich import print_json
import json


def explore_directory(directory_path, exclude_pattern=None):
    result = {"categories": []}
    base_directory = Path(directory_path).resolve()

    if exclude_pattern:
        exclude_regex = re.compile(exclude_pattern)

    for category_dir in base_directory.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            category_subdirs = []

            for sub_item in category_dir.iterdir():
                if sub_item.is_dir() and (
                    not exclude_pattern or not exclude_regex.match(sub_item.name)
                ):
                    subfiles = [f.name for f in sub_item.glob("*") if f.is_file()]
                    subdirs = [d.name for d in sub_item.glob("*") if d.is_dir()]

                    settings_file = sub_item / "project_settings.json"
                    if settings_file.is_file():
                        with open(settings_file, "r") as f:
                            data = json.loads(f.read())
                            pretty_name = data.get("name", "")
                            subdir_info = {
                                "project_name": sub_item.name,
                                "project_settings_path": str(settings_file.resolve()),
                                "pretty_name": pretty_name,
                            }
                            category_subdirs.append(subdir_info)

            category_info = {"category": category_name, "projects": category_subdirs}
            result["categories"].append(category_info)

    return result


# Example usage
if __name__ == "__main__":
    directory_path = "TestDir"
    exclude_pattern = r"^(\.gitignore|\.venv|\.git)$"

    result = explore_directory(directory_path, exclude_pattern)
    print_json(data=result)
