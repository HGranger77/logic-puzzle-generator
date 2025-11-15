import numpy as np
from models import Cell

cell_colours = {
    Cell.CROSS: "red",
    Cell.CROSS_INHERITED: "darkred",
    Cell.TICK: "green",
    Cell.MAYBE: "orange",
    Cell.EMPTY: "lightgrey"
}


class GridController():
    def __init__(self):
        self.category_count = 0
        self.category_size = 0
        self.grid_states = None
        self.grid_buttons = None
        self.grid_inheritence_counts = None


    def start_game(self, category_count: int, category_size: int):
        self.category_count = category_count
        self.category_size = category_size
        self.create_empty_grid()


    def create_empty_grid(self):
        shape = (self.category_count - 1, self.category_count - 1, self.category_size, self.category_size)
        self.grid_states = np.full(shape, Cell.EMPTY, dtype=object)
        self.grid_buttons = np.full(shape, None, dtype=object)
        self.grid_inheritence_counts = np.zeros(shape, dtype=int)

        for c1 in range(self.category_count - 1):
            for c2 in range(self.category_count - 1):
                if c1 < c2:
                    self.grid_states[c1, c2, :, :] = Cell.DEAD

    
    def bind_buttons(self):
        for i in range(self.category_count - 1):
            for j in range(self.category_count - 1):
                for ni in range(self.category_size):
                    for nj in range(self.category_size):
                        pos = (i, j, ni, nj)
                        button = self.grid_buttons[pos]
                        if button:
                            button.bind('<Button-1>', lambda _, p=pos: self.toggle_cell(p))
                            button.bind('<Button-2>', lambda _, p=pos: self.set_cell(p, Cell.MAYBE))
                            button.bind('<Button-3>', lambda _, p=pos: self.set_cell(p, Cell.EMPTY))


    def get_cell(self, position: tuple) -> Cell:
        return self.grid_states[position]


    def toggle_cell(self, position: tuple) -> Cell:
        current_cell = self.get_cell(position)
        next_cell = current_cell.next_member()
        self.set_cell(position, next_cell)
        return next_cell


    def set_cell(self, position: tuple, next_value: Cell):
        prev_value = self.get_cell(position)

        if prev_value == Cell.CROSS_INHERITED and self.grid_inheritence_counts[position] > 0:
            if next_value == Cell.CROSS_INHERITED:
                next_value = Cell.CROSS
            elif next_value == Cell.EMPTY or next_value == Cell.MAYBE:
                next_value = Cell.CROSS_INHERITED

        elif prev_value == Cell.TICK:
            self._update_inheritance(position, -1)

        elif (prev_value == Cell.CROSS or prev_value == Cell.MAYBE) and self.grid_inheritence_counts[position] > 0:
            next_value = Cell.CROSS_INHERITED

        self.grid_states[position] = next_value

        if next_value == Cell.TICK:
            self._update_inheritance(position, +1)

        colour = cell_colours[next_value]
        self.grid_buttons[position].config(bg=colour, activebackground=colour, fg=colour, activeforeground=colour)


    def _update_inheritance(self, position: tuple, delta: int):
        def iter_category_positions(position: tuple):
            category_box = position[0:2]
            for k in range(self.category_size):
                for idx in ((k, position[3]), (position[2], k)):
                    iter_pos = category_box + idx
                    if iter_pos != position:
                        yield iter_pos

        for iter_pos in iter_category_positions(position):
            self.grid_inheritence_counts[iter_pos] += delta
            if delta > 0:
                if self.get_cell(iter_pos) == Cell.EMPTY:
                    self.set_cell(iter_pos, Cell.CROSS_INHERITED)
            else:
                if self.grid_inheritence_counts[iter_pos] == 0 and self.get_cell(iter_pos) == Cell.CROSS_INHERITED:
                    self.set_cell(iter_pos, Cell.EMPTY)
