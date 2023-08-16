
from pathlib import Path
import re
from time import sleep
from src import explore_directory, Project, Menu

from rich import print as rprint
from rich import print_json
from rich.prompt import Prompt
from rich.console import Console
from rich.status import Status
from os import get_terminal_size

ROOT_DIR = r"C:\Users\Antho\Desktop\Projects\Etc\Project manager\TestDir"


con = Console()
class Main:
    def __init__(self, project_info: dict = None) -> None:
        self.project_info = project_info
        if project_info is None:
            self.project_info = explore_directory(ROOT_DIR)
        
        self.projects = []

    
    def resfresh(self):
        self.project_info = explore_directory(ROOT_DIR)
    
    def get_all_project_info(self, setting_path:str|Path):
        pass
    
    def find_project(self, indentifier:str, category:str):
        self.resfresh()
        projects = self.project_info.copy()
        print_json(data=projects['categories'])
        for i in projects['categories']:
            curr_category = i.get('category')
            if curr_category == category:
                # print(i)
                for item in i[curr_category]['projects']:
                    if item['project_name'] == indentifier:
                        p = None
    
    def init_project(self, name: str, description: str, tags: list, category: str):
        identifier = name.replace(" ", "-").lower()
        resp = self.get_project(identifier)

        if resp is not None:
            self.projects.remove(resp)

        project = Project(name, identifier, description, tags, category, ROOT_DIR)
        project.save()
        self.projects.append(project)
        self.resfresh()

       

    def get_project(self, identifier: str):
        
        for i in self.projects:
            if i.identifier == identifier:
                return i
        return None

    def print_projects(self):
        print("Projects:")
        for i in self.projects:
            print(f"\t{i}")
    
    def remove_project(self, identifier: str, category: str):
        categories = sorted([i["category"] for i in self.project_info["categories"]])

        if category not in categories:
            return False
        
        
        self.resfresh()

class TUI:
    def __init__(self, main_instance:Main) -> None:
        self.main = main_instance

    def create_project(self):
        with con.screen() as screen:
            rprint("[bold green]Create Project[/]")
            name = Prompt.ask("Name")
            description = Prompt.ask("Description")
            category = Prompt.ask("Category")
            tags = Prompt.ask("Tags (seperated by ',')").split(", ")
            con.clear()
            rprint("[bold green]Create Project[/]")
            rprint("[bold red]Please confirm this infromation")
            print("Name:", name)
            print("Description:", description)
            print("Category", category)
            print("Tags:")
            for i in tags:
                print(f"\t{i}")
            ans = Prompt.ask("Is this info correct?", choices=['yes', 'no', 'y', 'n'])
           
        
        

            
        

if __name__ == "__main__":
    while True:
        main = Main(explore_directory(ROOT_DIR))
        main.resfresh()
        
        t = TUI(main)
        menu = Menu("Project Manager", [('Create Project', t.create_project)])
        menu.show()
        