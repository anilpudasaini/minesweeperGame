# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:25:24 2023

@author: Anil
"""
from tkinter import Button, Label
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count_label_object = None
    cell_count = settings.CELL_COUNT

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
            # text=f"{self.x},{self.y}"
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)

        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def get_cell_by_axis(self, x, y):
        # Returns a cell based on the values of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:  # if no mines then show surrounding cells
                for cell_obj in self.surrounding_cells:
                    cell_obj.show_cell()

            self.show_cell()
            # Game wining case
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(
                    0, 'Congratulations!! You Win', 'Winner', 0)
                sys.exit()

        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    @property
    def surrounding_cells(self):
        # need to get all the surrounding mines and display it
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cells in self.surrounding_cells:
            if cells.is_mine:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(
                text=self.surrounded_cells_mines_length)
            # replace the label count with new count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this was a mine candidate then for safety config btn face to syste, default
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )

        # Mark the cell as opened (Use is as the last line of this method)
        self.is_opened = True

    def show_mine(self):
        # logic to show mine and end the game
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(
            0, 'You stepped on a mine', 'Game Over', 0)
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for each in picked_cells:
            each.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
