from json import dumps
import shutil
import os
from pathlib import Path


class Project:
    def __init__(
        self,
        name=None,
        identifier=None,
        description=None,
        tags=None,
        category=None,
        root_dir="./TestDir/",
        scripts=dict,
    ):
        self.name = name
        self.identifier = identifier
        self.description = description
        self.tags = tags or []
        self.category = category
        self.scripts = scripts

        if scripts == dict:
            self.scripts = {}
        self.project_file = (
            Path(root_dir)
            .joinpath(category, identifier, "project_settings.json")
            .absolute()
        )

    def set_name(self, new_name, replace_identifier=True):
        self.name = new_name
        if replace_identifier:
            self.identifier = new_name.replace(" ", "-").lower()
        self.save()

    def as_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "identifier": self.identifier,
            "tags": self.tags,
            "scripts": self.scripts,
        }

    def save(self):
        if not self.project_file:
            print(f"Invalid file: {self}")
            return

        if not self.project_file.exists():
            os.makedirs(str(self.project_file).removesuffix("project_settings.json"))

        with open(self.project_file, "w+") as f:
            f.write(dumps(self.as_json(), indent=4))

    def delete(self):
        if not self.project_file:
            print(f"Invalid file: {self}")
            return

        if not self.project_file.exists():
            print(f"Project doesn't exist: {self}")
            return

        path_to_delete = self.project_file.parent
        shutil.rmtree(path_to_delete)

    def __str__(self):
        return (
            f'Project(name="{self.name}", identifier="{self.identifier}", '
            f'description="{self.description}", tags={self.tags}, category="{self.category}")'
        )


if __name__ == "__main__":
    p = Project(
        "Test Project 2", category="other", root_dir="./TestDir/", identifier="test"
    )
    p.save()
    p.delete()
