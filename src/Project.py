from json import dumps
import os
from pathlib import Path


class Project:
    def __init__(self, name:str=None, identifier=None, description=None, tags=[], category=None, root_dir="./TestDir/") -> None:
        if name is not None:
            self.name = name
            if identifier is None:
                self.identifier = name.replace(" ", "-").lower()
        self.description = description
        self.tags = tags
        self.category = category
        self.project_file = Path(root_dir).joinpath(category).joinpath(self.identifier).joinpath('project_settings.json').absolute()
    def set_name(self, new_name:str, replace_indentifier=True):
        self.name == new_name
        if replace_indentifier:
            self.identifier = new_name.replace(" ", "-").lower()
        self.save()
    def as_json(self):
        return {'name': self.name, 'description': self.description, 'identifier': self.identifier, 'tags': self.tags}
    
    def save(self):
        if self.project_file is None:
            print(f"Invalid file: \n\tClass: '{str(self)}'")
            return
        if not self.project_file.exists():
            os.makedirs(str(self.project_file).removesuffix('project_settings.json'))
        with open(self.project_file, 'w+') as f:
            f.write(dumps(self.as_json()))
    
    def __str__(self) -> str:
        return f"Project(name={self.name}, identifier={self.identifier}, description={self.description}, tags={self.tags}, category={self.category}, project_file={self.project_file})"
                
if __name__ == "__main__":
    p = Project("Test Project", category="Python")
    
    
    p.save()