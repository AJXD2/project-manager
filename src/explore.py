import re
from pathlib import Path
from rich import print_json

def explore_directory(directory_path, exclude_pattern=None):
    result = {'categories': []}
    base_directory = Path(directory_path).resolve()
    
    if exclude_pattern:
        exclude_regex = re.compile(exclude_pattern)
    
    for category_dir in base_directory.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            
            # Explore second level directories within the category
            category_subdirs = []
            for sub_item in category_dir.iterdir():
                if sub_item.is_dir():
                    if exclude_pattern and exclude_regex.match(sub_item.name):
                        continue  # Skip excluded directories
                    
                    subfiles = [f.name for f in sub_item.glob('*') if f.is_file()]
                    subdirs = [d.name for d in sub_item.glob('*') if d.is_dir()]
                    
                    # Look for 'project_settings.json' file
                    settings_file = sub_item / 'project_settings.json'
                    if settings_file.is_file():
                        settings_path = str(settings_file.resolve())
                    else:
                        settings_path = None
                    
                    subdir_info = {
                        'project_name': sub_item.name,
                        'project_settings_path': settings_path
                    }
                    category_subdirs.append(subdir_info)
            
            category_info = {
                'category': category_name,
                'projects': category_subdirs
            }
            result['categories'].append(category_info)
    
    return result

# Example usage
if __name__ == "__main__":
    directory_path = 'TestDir'
    exclude_pattern = r'^(\.gitignore|\.venv|\.git)$'
    
    result = explore_directory(directory_path, exclude_pattern)
    print_json(data=result)
