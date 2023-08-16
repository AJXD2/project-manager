from json import dumps
import shutil
import os
from pathlib import Path


class Project:
    def __init__(self, name:str=None, identifier=None, description=None, tags=[], category=None, root_dir="./TestDir/") -> None:
    
        self.name = name
        self.identifier = identifier
    
        self.description = description
        self.tags = tags
        self.category = category
        self.project_file = Path(str(root_dir)).joinpath(category).joinpath(self.identifier).joinpath('project_settings.json').absolute()
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
    def delete(self):
        if self.project_file is None:
            print(f"Invalid file: \n\tClass: '{str(self)}'")
            return
        if not self.project_file.exists():
            print(f"Project doesnt exist: \n\tClass: '{str(self)}'")
            return
        
        path_to_delete = self.project_file.parent
        shutil.rmtree(path_to_delete)
    def __str__(self) -> str:
        return f'Project(name="{self.name}", identifier="{self.identifier}", description="{self.description}", tags={self.tags}, category="{self.category}"'
                
if __name__ == "__main__":
    p = Project("Test Project 2", category="other", root_dir="./TestDir/", identifier="test")
    
    
    p.save()
    p.delete()