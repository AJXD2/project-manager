from json import loads
from pathlib import Path
import sys
from time import sleep
from src import explore_directory, Project, Menu, Main
from rich.prompt import Prompt
from rich.console import Console
from rich.tree import Tree
from rich.status import Status
from rich import print as rprint, print_json
from dotenv import load_dotenv
import os

load_dotenv()
DEBUG = os.environ.get("debug")
ROOT_DIR = r"C:\Users\Antho\Desktop\Projects\Etc\Project manager\TestDir"

con = Console()


class TUI:
    def __init__(self, main_instance):
        self.main = main_instance

    def create_project(self):
        with con.screen() as screen:
            con.print("[bold green]Create Project[/]")
            name = Prompt.ask("Name")
            description = Prompt.ask("Description")
            category = Prompt.ask("Category")
            tags = Prompt.ask("Tags (REQUIRED) (separated by ',')").split(", ")
            if tags == [""]:
                tags = []
                rprint(
                    "[red bold]You need to have at least one tag followed by a comma"
                )
                sleep(3)
                return
            con.clear()
            con.print("[bold green]Create Project[/]")
            con.print("[bold red]Please confirm this information")
            con.print("Name:", name)
            con.print("Description:", description)
            con.print("Category", category)
            con.print("Tags:")
            for tag in tags:
                con.print(f"\t{tag}")
            ans = Prompt.ask("Is this info correct?", choices=["yes", "no", "y", "n"])
            with con.status("Creating Project...", spinner="material"):
                project = self.main.init_project(name, description, tags, category)
                project.save()
            con.clear()
            con.print("[bold green]Saved!")
            sleep(2)
            return

    def delete_project(self):
        with con.screen() as screen:
            con.print("[bold red]Delete Project[/]")
            name = Prompt.ask("Name")
            category = Prompt.ask("Category")
            con.clear()
            con.print("[bold red]Delete Project[/]")
            con.print("[bold red]Please confirm this information")
            con.print("Name:", name)
            con.print("Category", category)
            ans = Prompt.ask("Is this info correct?", choices=["yes", "no", "y", "n"])
            if ans not in ["y", "yes"]:
                return
            project = self.main.get_project(self.main.name_to_ident(name))
            if project is None:
                rprint(
                    f"[red bold]Project doesnt exist '{self.main.name_to_ident(name)}'"
                )
                sleep(2)
                return
            elif project is not None:
                project.delete()
            con.clear()
            con.print("[bold red]Deleted!")
            sleep(2)
            return

    def list_projects(self):
        with con.screen():
            data = self.main.project_info
            tree = Tree("Projects")

            for category_data in data["categories"]:
                category = tree.add(category_data["category"])
                for project_data in category_data["projects"]:
                    project_name = project_data["pretty_name"]
                    project = category.add(project_name)
                    project.add(f"Name: {project_name}")

            con.print(tree)

            Prompt.ask("Press enter to continue...")


if __name__ == "__main__":
    main = Main(explore_directory(ROOT_DIR))
    t = TUI(main)
    options = [
        ("Create Project", t.create_project),
        ("Delete Project", t.delete_project),
        ("List Projects", t.list_projects),
        ("Exit", sys.exit),
    ]
    while True:
        main.refresh()
        with con.screen():
            menu = Menu("Project Manager", options)
            menu.show()
