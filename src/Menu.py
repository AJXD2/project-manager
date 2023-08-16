import os
from rich import print
from rich.prompt import Prompt
class Menu:
    def __init__(self, title:str,  options:list, subtitle:str=None) -> None:
        """
            title:str Ttile of menu
            options:list List of options (eg: options=[("play", play), ("exit", exit)])
            subtitle:str Subtitle
        """
        self.title= title
        self.options = options
        self.subtitle = subtitle

    def show(self):
        
        print(f"\t\t{self.title}\n")
        for i in self.options:
            print(f"\t\t{self.options.index(i) + 1}. {i[0]}")
        print("\n")
        p = Prompt().ask("\tSelect an option from the list above", choices=[str(self.options.index(i) + 1) for i in self.options])
        
        ans = self.options[int(p)-1][1]
        ans()    


if __name__ == "__main__":
    def foo():
        print("foo")
        
    def bar():
        print("bar")
    m = Menu("Title", [("foo", foo),("bar", bar)], "Subtitle")
    m.show()