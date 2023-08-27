from os import system
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
            print(
                f"{i+1} [{item.category}/{item.identifier}] - {item.name} - {item.description:.10}"
            )


if __name__ == "__main__":
    main.refresh()
    fire.Fire(CLI)
