from rich import print
from rich.prompt import Prompt


class Menu:
    def __init__(self, title, options, subtitle=None):
        self.title = title
        self.options = options
        self.subtitle = subtitle

    def show(self):
        print(f"\t\t{self.title}\n")
        for index, option in enumerate(self.options, start=1):
            print(f"\t\t{index}. {option[0]}")
        print("\n")
        selected_option = Prompt.ask(
            "\tSelect an option from the list above",
            choices=[str(i) for i in range(1, len(self.options) + 1)],
        )
        selected_function = self.options[int(selected_option) - 1][1]
        selected_function()


if __name__ == "__main__":

    def foo():
        print("foo")

    def bar():
        print("bar")

    m = Menu("Title", [("foo", foo), ("bar", bar)], "Subtitle")
    m.show()
