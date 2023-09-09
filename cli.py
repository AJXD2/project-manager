import enum
import json
from os import system
from pathlib import Path
import sys
import fire
from src import Main
from src import explore_directory

main = Main(explore_directory("/Users/Antho/Desktop/Projects/Etc/Project manager"))


class CLI(object):
    """Project Manager"""

    def create(self, name, category, description="My new project", tags=["project"]):
        if tags == True:
            tags = ["project"]

        project = main.init_project(name, description, tags, category)
        project.save()

    def delete(self, name_or_identifier):
        ident = main.name_to_ident(name_or_identifier)

        project = main.find_project(ident)

        project.delete()

    def usevscode(self, name_or_identifier):
        ident = main.name_to_ident(name_or_identifier)

        project = main.get_project(ident)
        if project == None:
            print("[X] Project Not Found!")
            exit()
        project_path = str(project.project_file).removesuffix("project_settings.json")

        system("cd {0} && code .".format(project_path))

    def lsprojects(self, category):
        d = main.projects

        for i, item in enumerate(d):
            if item.category == category:
                print(
                    f"{i+1} [{item.category}/{item.identifier}] - {item.name} - {item.description:.10}"
                )

    def run(self, script):
        path = Path("./project_settings.json")

        if path.exists():
            with path.open("r") as f:
                data = json.loads(f.read())

            scripts_obj = data.get("scripts")
            if scripts_obj is None:
                print("Error: Project file error. No script object found!")
                return

            command = scripts_obj.get(script)

            if command == None:
                print(
                    f"Error: No script with name '{script}' found in current config file!"
                )
                sys.exit()

            if isinstance(command, list):
                for index, cur in enumerate(command):
                    print(f"Running command: '{cur}' ({index + 1}/{len(command)})")
                    system(cur)
                return
            system(command)
        else:
            print("Error: No project file found in current directory!")
            sys.exit()


if __name__ == "__main__":
    main.refresh()
    fire.Fire(CLI)
