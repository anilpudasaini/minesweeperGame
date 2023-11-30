# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:25:24 2023

@author: Anil
"""
from tkinter import Button
import random
import settings


class Cell:
    all = []

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
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

    def get_cell_by_axis(self, x, y):
        # Returns a cell based on the values of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()

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
        self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)

    def show_mine(self):
        # logic to show mine and end the game
        self.cell_btn_object.configure(bg="red")

    def right_click_actions(self, event):
        print(event)
        print("RIGHT")

    @ staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for each in picked_cells:
            each.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
