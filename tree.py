# IMPORTS
import os
import random
import re
import time
from collections import deque
from math import ceil

import colorama
from colorama import Back, Fore, Style

colorama.init(autoreset=True)


# CLASS
class ChristmasTree:
    def __init__(self, add_tree_lines=12, light_type="r"):
        self.tree = []
        self.light_tree = []

        self.add_tree_lines = add_tree_lines

        # for patternized light_type ("p")
        self.light_colors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.YELLOW]
        self.light_type = light_type
        self.light_color_idx = 0

    def _switch(self, sep):
        """
        Switches the seperator design, for the middle parts, in the tree.

        Args:
            sep (str): seperator design.

        Returns:
            str: seperator
        """
        return "\\" if sep == "/" else "/"

    def _add_outline(self, middle):
        """
        Add the edges to the middle part of the line.

        Args:
            middle (str): Middle part of a line in the tree.

        Returns:
            str: Completed line of the tree.
        """
        return f"/{middle}\\"

    def _add_line(self, line_length, sep):
        """Adds a completed line to the tree.

        Args:
            line_length (int): length of the line.
            sep (str): seperator design for middle parts.
        """
        middle_length = line_length - 2
        middle = list(sep.join(["_"] * ceil(middle_length / 2)))
        if sep == "/":
            if middle.count("_") % 2 == 0:
                middle[0] = middle[-1] = "●"
            else:
                for i in range(0, len(middle), 4):
                    middle[i] = "●"
        middle = "".join(middle)
        line = self._add_outline(middle)
        self.tree.append(line)

    def _get_light_color(self):
        """Picks a light color, based on user's light type.

        Returns:
            colorama.FORE: the ANSI color code type for the light.
        """
        if self.light_type == "r":
            return random.choice(self.light_colors)
        elif self.light_type == "p":
            return self.light_colors[self.light_color_idx % len(self.light_colors)]
        else:
            return Fore.WHITE

    def _colorify(self, line):
        """Let's spruce up that black & white Christmas tree.

        Args:
            line (str): a line in the christmas tree.

        Returns:
            str: the colorfied line of the christmas tree.
        """
        base = re.search(r"\|_+\|", line)
        line = list(line)
        light_flag = False

        for idx, ele in enumerate(line):
            if ele == "*":
                line[
                    idx
                ] = f"{Style.BRIGHT}{Fore.YELLOW}{ele}{Fore.RESET}{Style.NORMAL}"
            elif ele == "|":
                line[idx] = f"{Fore.CYAN}{ele}{Fore.RESET}"
            elif ele == "_" and base:
                line[idx] = f"{Fore.CYAN}{ele}{Fore.RESET}"
            elif ele == "●":
                color = self._get_light_color()
                line[idx] = f"{Style.BRIGHT}{color}{ele}{Fore.RESET}{Style.NORMAL}"
                light_flag = True
            else:
                line[idx] = f"{Fore.GREEN}{ele}{Fore.RESET}"

        self.light_color_idx += light_flag
        return f'{Back.BLACK}{"".join(line)}{Back.RESET}'

    def _add_padding(self, tree):
        """Adds center justification to the tree lines.

        Args:
            tree (list): the christmas tree.

        Returns:
            list: the center justified christmas tree.
        """
        longest_line_length = len(max(tree, key=len))
        padding = longest_line_length + 2
        padded_tree = [line.center(padding) for line in tree]
        return padded_tree

    def generate_tree(self):
        """
        Generate Christmas Tree

        Returns:
            List[str]: the christmas tree
        """
        sep = "\\"
        line_length = 1

        # Create star of tree
        star = ["*", "*" * 3]
        self.tree.extend(star)

        # Generate top part of the tree (3 lines)
        for _ in range(3):
            line_length += 2
            sep = self._switch(sep)
            self._add_line(line_length, sep)

        # Generate rest of the tree
        for _ in range(0, self.add_tree_lines, 2):
            # Line 1 of A Part
            sep = self._switch(sep)
            self._add_line(line_length, sep)

            # Line 2 of A Part
            sep = self._switch(sep)
            line_length += 2
            self._add_line(line_length, sep)

        # Generate trunk of tree
        girth = 3
        trunk = (" " * girth).join(["|", "|"])
        base = ("_" * girth).join(["|", "|"])
        self.tree.append(trunk)
        self.tree.append(base)

    def _message(self):
        """Displays a sliding window of a chosen message: "MERRY CHRISTMAS AND HAPPY NEW YEAR!"

        Yields:
            str: the current sliding window of the message
        """
        window_length = len(max(self.tree, key=len))
        color_window_length = window_length
        max_color_window_length = window_length * 11
        window = deque(maxlen=window_length)

        msg = " MERRY CHRISTMAS AND HAPPY NEW YEAR!" + (" " * (window_length // 2))
        msg_iter = iter(msg)

        colors = [Fore.RED, Fore.WHITE, Fore.GREEN]
        color_idx = 0

        while True:
            try:
                letter = next(msg_iter)
            except StopIteration:
                msg_iter = iter(msg)
                letter = next(msg_iter)

            colored_letter = f"{colors[color_idx % len(colors)]}{letter}{Fore.RESET}"
            color_idx += letter != " "
            window.append(colored_letter)
            color_window_length += (
                10 if color_window_length < max_color_window_length else 0
            )
            window_msg = "".join(window).rjust(color_window_length)

            yield "\n".join(
                [
                    f"{Back.BLACK}{' ' * window_length}{Back.RESET}",
                    f"{Back.BLACK}{window_msg}{Back.RESET}",
                ]
            )

    def start(self):
        """
        LET THE LIGHT SHOW BEGIN!!!
        """
        self.tree = self._add_padding(self.tree)
        self.light_tree = self.tree.copy()
        window_msg = self._message()

        while True:
            for idx, line in enumerate(self.tree):
                light_line = self._colorify(line)
                self.light_tree[idx] = light_line

            os.system("cls" if os.name == "nt" else "clear")
            print("\n".join(self.light_tree))
            print(next(window_msg))

            self.light_colors = rotate(self.light_colors)
            self.light_color_idx = 0
            time.sleep(0.5)


# FUNCTIONS
def rotate(arr, k=1):
    """Rotate an array by k times to the right.

    Args:
        arr (list): the array
        k (int, optional): rotate by how much. Defaults to 1.

    Returns:
        list: the rotated array
    """
    return arr[-k:] + arr[:-k]


def valid_input(input_):
    """Check if input is a positive even number.

    Args:
        input_ (any): user input

    Returns:
        bool: whether input is a positive even number.
    """
    try:
        input_ = int(input_)
    except ValueError:
        return False

    if input_ <= 0 or input_ % 2 != 0:
        return False

    return True


# MAIN

# User Inputs
# note: this base_tree is NOT a part of the actual Christmas tree generated, rather just to show the user what we are working with.
base_tree = """
           *
          ***
          /_\\
         /_\_\\
        /_/_/_\\
         |   |
         |___|"""
input_msg = """
Welcome to my Christmas Tree generator! Above is our current Christmas tree right now.
It seems pretty small to me, so let's add some length to it!
Let's shoot for a positive even number somewhere between 2 to 26 (you are more than welcome to aim for bigger even numbers, but don't blame me if something goes wrong ¯\_(ツ)_/¯).

Enter a positive even number: """
print(base_tree)
add_lines = input(input_msg)

while not valid_input(add_lines):
    print("Seems like this is not a positive even number. Let's try again!")
    add_lines = input("Enter a positive even number: ")

print()
light_type = input("What light type do you want? Randomized or Patternized? (r/p): ")
while light_type not in ["r", "p"]:
    light_type = input("Enter either 'r' or 'p': ")

# Fun Little Teaser
print("\nGenerating your Christmas Tree", end="")
for _ in range(4):
    print(".", end="")
    time.sleep(1)

# Class Instantiation
tree = ChristmasTree(int(add_lines), light_type)
tree.generate_tree()
tree.start()
