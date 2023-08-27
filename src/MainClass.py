from typing import List
from rich import print as rprint, print_json
from rich.console import Console
from json import loads
from dotenv import load_dotenv
import os
from . import explore_directory, Project

load_dotenv()
DEBUG = os.environ.get("debug")
ROOT_DIR = r"C:\Users\Antho\Desktop\Projects\Etc\Project manager\TestDir"

con = Console()


class Main:
    def __init__(self, project_info=None):
        self.project_info = project_info
        if project_info is None:
            self.project_info = explore_directory(ROOT_DIR)

        self.projects = []

    def refresh(self, without_projects=False):
        self.project_info = explore_directory(ROOT_DIR)
        if without_projects:
            return
        projects = self.project_info.copy()
        for category_info in projects["categories"]:
            curr_category = category_info.get("category")
            for item in category_info["projects"]:
                with open(item["project_settings_path"], "r") as f:
                    data = loads(f.read())
                p = self.init_project(**data, category=curr_category)

    def find_project(self, identifier, category):
        self.refresh()
        projects = self.project_info.copy()
        p = None
        for category_info in projects["categories"]:
            curr_category = category_info.get("category")
            if curr_category == category:
                for item in category_info[curr_category]["projects"]:
                    if item["project_name"] == identifier:
                        with open(item["project_settings_path"], "r") as f:
                            p = self.init_project(**loads(f.read()))

        return p

    def init_project(
        self, name, description, tags, category, identifier=None, scripts=dict
    ):
        if identifier is None:
            identifier = self.name_to_ident(name)
        resp = self.get_project(identifier)

        if resp is not None:
            self.projects.remove(resp)

        project = Project(
            name, identifier, description, tags, category, ROOT_DIR, scripts
        )
        project.save()
        self.projects.append(project)
        self.refresh(without_projects=True)
        return project

    def get_project(self, identifier) -> Project | None:
        for proj in self.projects:
            if proj.identifier == identifier:
                return proj
        return None

    def remove_project(self, identifier, category):
        categories = sorted([i["category"] for i in self.project_info["categories"]])

        if category not in categories:
            return False

        self.refresh()

    def name_to_ident(self, name):
        return name.replace(" ", "-").lower()
