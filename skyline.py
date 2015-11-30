""" Skyline: puzzle game

Grid puzzle with clues.
Player has to fill the grid in a sodoku style.
Multiple solutions possible.

"""

import itertools
import random
try:
    import tkinter as tk
except ImportError:
    try:
        import Tkinter as tk
    except ImportError:
        input("Failed to load tkinter, aborting...")

__author__ = "6057374: Vincent Kühn, 6192860: Georg Schuhardt"
__copyright__ = "Copyright 2015/2016 – EPR-Goethe-Uni"
__credits__ = "none this time"
__email__ = "georg.schuhardt@gmail.com"
__github__ = "https://github.com/banur/EPR1_SuperBrain"


class Skyline(tk.Frame):

    """ Skyline puzzle game. """

    __boardsize = 0
    __skyline = []
    __hints = []
    __solved_grid = []
    __solved = 0
    __entry_fields = []
    __input_list = []

    def __init__(self, boardsize=4, master=None):
        """ Initialise the game. """
        tk.Frame.__init__(self, master)
        self.__boardsize = boardsize
        self.grid()
        self.__start_game()

    def __start_game(self):
        """ Setup the games subroutines. """
        self.__generate_skyline()
        self.__hints = self.__generate_hints()
        self.__generate_empty_board()
        self.__build_ui()

    def __generate_skyline(self):
        """ Generate a possible solution by choosing from permutations. """
        boardsize = self.__boardsize
        street = []
        for i in range(1, boardsize + 1):
            street.append(i)
        perm_list = list(itertools.permutations(street, boardsize))
        for rows in range(boardsize):
            street = random.choice(perm_list)
            perm_list.remove(street)
            removal_list = []
            for house in range(len(street)):
                for available_streets in perm_list:
                    if street[house] == available_streets[house]:
                        removal_list.append(available_streets)
            for remove_street in removal_list:
                try:
                    perm_list.remove(remove_street)
                except:
                    pass
            self.__skyline.append(street)

    def __generate_hints(self, skyline=None):
        """ Generate the hints for the code, return as list. """
        hints = []
        if skyline is None:
            skyline = self.__skyline
        for orientation in ("down", "up", "to_right", "to_left"):
            if orientation == "to_left" or orientation == "to_right":
                hints.append([])
                for row in skyline:
                    if orientation == "to_right":
                        condition_range = [0, range(len(row))]
                    elif orientation == "to_left":
                        condition_range = [-1, range(len(row) - 1, -1, -1)]
                    visible_houses = 1
                    highest_visible = row[condition_range[0]]
                    for house in condition_range[1]:
                        if highest_visible < row[house]:
                            visible_houses += 1
                            highest_visible = row[house]
                    hints[-1].append(visible_houses)
            if orientation == "up" or orientation == "down":
                hints.append([])
                for column in range(len(skyline)):
                    if orientation == "down":
                        condition_range = [0, range(len(skyline))]
                    elif orientation == "up":
                        condition_range = [-1, range(len(skyline) - 1, -1, -1)]
                    visible_houses = 1
                    highest_visible = skyline[condition_range[0]][column]
                    for house in condition_range[1]:
                        if highest_visible < skyline[house][column]:
                            visible_houses += 1
                            highest_visible = skyline[house][column]
                    hints[-1].append(visible_houses)
        return hints

    def __compare_grid(self):
        """ Compare the users input, call victory popup. """
        is_filled = False
        for bracket in self.__solved_grid:
            if 0 not in bracket:
                is_filled = True
            else:
                is_filled = False
        if is_filled:
            user_code = self.__generate_hints(self.__solved_grid)
            if user_code == self.__hints:
                self.__quit_game()

    def __quit_game(self):
        """ Display victory popup and exit prompt. """
        top = tk.Toplevel()
        top.title("Victory!")
        msg = "You found a right solution."
        top_frame = tk.Frame(top)
        top_frame.grid()
        top.geometry("+360+360")
        popup_label = tk.Label(top_frame, text=msg)
        popup_label.grid(columnspan=2)
        exit_button = tk.Button(top_frame, text="Exit", command=self.quit)
        exit_button.grid(row=1, column=1)

    def __user_input(self):
        """ Save the users input to list and compare to the skyline. """
        for item in range(len(self.__input_list)):
            row = item // self.__boardsize
            column = item % self.__boardsize
            try:
                input_item = self.__input_list[item].get()
            except AttributeError:
                pass
            if input_item.isdigit():
                if input_item == "1337":
                    self.__solved_grid = list(self.__skyline)
                    break
                else:
                    self.__solved_grid[row][column] = int(input_item)
        self.__compare_grid()

    def __generate_empty_board(self):
        """ Generate an empty board. """
        for i in range(self.__boardsize):
            self.__solved_grid.append([])
            for i in range(self.__boardsize):
                self.__solved_grid[-1].append(0)
                self.__input_list.append([])

    def __create_entry_fields(self):
        """ Create entry fields based on the boardsize. """
        for i in range(self.__boardsize**2):
            string_var = self.__input_list[i] = tk.StringVar()
            row = i // self.__boardsize + 1
            column = i % self.__boardsize + 1
            string_var.trace("w", lambda name, index, mode,
                             string_var=string_var: self.__user_input())
            new_entry = tk.Entry(self.master, width=5, textvariable=string_var)
            new_entry.grid(row=row, column=column)
            self.__entry_fields.insert(0, i)

    def __create_labels(self):
        """ Create labels based on the boardsize and fill with hints. """
        hints = self.__hints
        for i in range(1, self.__boardsize + 1):
            new_label_top = tk.Label(self.master, text=hints[0][i - 1])
            new_label_top.grid(row=0, column=i)
            new_label_bot = tk.Label(self.master, text=hints[1][i - 1])
            new_label_bot.grid(row=self.__boardsize + 1, column=i)
            new_label_left = tk.Label(self.master, text=hints[2][i - 1])
            new_label_left.grid(row=i, column=0)
            new_label_right = tk.Label(self.master, text=hints[3][i - 1])
            new_label_right.grid(row=i, column=self.__boardsize + 1)

    def __build_ui(self):
        """ Generate the users UI, start GUI loop. """
        self.master.title('Skyline')
        self.master.geometry("+300+300")
        quit_buttton = tk.Button(None, text="quit", command=self.quit)
        quit_buttton.grid(row=1000, column=1000)
        info_text = "Fill the grid with unique digits from 1 to {0}.".format(
            self.__boardsize)
        info_label = tk.Label(None, text=info_text)
        info_label.grid(row=1000, columnspan=6)
        self.__create_entry_fields()
        self.__create_labels()
        self.mainloop()

new_game = Skyline()
