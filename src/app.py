import tkinter as tk
from tkinter import ttk

from grid import GridController
from widgets import SpinboxWithMemory, HintLabelFrame

CAT_ITEMS = ["Lemon", "Grape", "Apple", "Orange", "Pear"]
HINTS = ["The lemon is a lemon", "The grape is a grape", "The apple is not the orange", "The pear is next to the banana", "The mango is above the peach"]


class LogicoApp(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Logic Puzzle")

        self.top_frames = [tk.Frame]
        self.game_controller = GridController()

        self._create_controls_widget()
        self._create_game_widget()
        self._show_frame(self.control_frame)


    def _show_frame(self, frame_to_show: tk.Frame):
        for f in self.top_frames:
            try:
                if f is frame_to_show:
                    if not f.winfo_ismapped():
                        f.pack(fill='both', expand=True)
                else:
                    if f.winfo_ismapped():
                        f.pack_forget()
            except Exception:
                pass


    def _create_controls_widget(self):
        self.control_frame = ttk.Frame(self, padding="10")
        self.top_frames.append(self.control_frame)

        self.spinbox_frame = ttk.Frame(self.control_frame, padding="10")
        self.spinbox_frame.grid(row=0, column=0, padx=5)

        self.category_size_value = tk.StringVar(value="4")
        self.category_count_value = tk.StringVar(value="3")

        self.category_size_label = ttk.Label(self.spinbox_frame, text="Category size:")
        self.category_size_label.grid(row=0, column=0, padx=5, sticky='w')

        self.category_size_display = SpinboxWithMemory(
            self.parent, self.spinbox_frame, textvariable=self.category_size_value, width=2
        )
        self.category_size_display.grid(row=0, column=1, padx=5)

        self.category_count_label = ttk.Label(self.spinbox_frame, text="Category count:")
        self.category_count_label.grid(row=1, column=0, padx=5, sticky='w')

        self.category_count_display = SpinboxWithMemory(
            self.parent, self.spinbox_frame, textvariable=self.category_count_value, width=2
        )
        self.category_count_display.grid(row=1, column=1, padx=5)

        ttk.Button(self.control_frame, text="Create Grids", command=self.start_game).grid(row=1, column=0, padx=5)


    def _create_game_widget(self):
        self.game_frame = ttk.Frame(self, padding="10")
        self.top_frames.append(self.game_frame)

        self.grid_frame = ttk.Frame(self.game_frame, padding="10")
        self.grid_frame.grid(row=0, column=0, padx=5)

        ttk.Separator(self.game_frame, orient="vertical").grid(column=1, row=0, rowspan=3, sticky='ns')

        self.hint_frame = ttk.Frame(self.game_frame, padding="10")
        self.hint_frame.grid(row=0, column=2, padx=5, sticky='n')

        ttk.Button(self.game_frame, text="Return", command=lambda: self._show_frame(self.control_frame)).grid(row=1, column=2, padx=5, sticky='e')


    def start_game(self):
        category_count=int(self.category_count_value.get())
        category_size=int(self.category_size_value.get())
        self.game_controller.start_game(category_count, category_size)
        self.create_grid_display(category_count, category_size)
        self.create_hint_display()
        self._show_frame(self.game_frame)


    def create_grid_display(self, category_count: int, category_size: int):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        c = category_count - 1
        n = category_size

        canvas_width = 50
        canvas_height = 33

        for i in range(c):
            frame = tk.Frame(self.grid_frame)
            frame.grid(row=i, column=0)
            for i in range(n):
                canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg="#D9D9D9")
                canvas.grid(row=i, column=0)
                canvas.create_text(canvas_width, canvas_height/2, text=f" {CAT_ITEMS[i]} ", angle=0, anchor='e')

        for i in range(c):
            for j in range(i+1):
                frame = tk.Frame(self.grid_frame, highlightbackground="grey", highlightthickness=5)
                for ni in range(n):
                    for nj in range(n):
                        grid_cell_frame = tk.Frame(frame, highlightbackground="black", highlightthickness=5)
                        grid_cell_frame.grid(row=ni, column=nj)
                        button = tk.Button(grid_cell_frame, text=" ")
                        button.pack()
                        self.game_controller.grid_buttons[i,j,ni,nj] = button
                frame.grid(row=i, column=j+1)
        self.game_controller.bind_buttons()

        canvas_width = 40
        canvas_height = 50

        for j in range(c):
            frame = tk.Frame(self.grid_frame)
            frame.grid(row=c+1, column=j+1)
            for i in range(n):
                canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg="#D9D9D9")
                canvas.grid(row=0, column=i)
                canvas.create_text(canvas_width/2, 0, text=f" {CAT_ITEMS[i]} ", angle=90, anchor='e')


    def create_hint_display(self):
        for widget in self.hint_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.hint_frame, text="Hints:", wraplength=200).grid(row=0, column=0, sticky='w', pady=(0, 15))
 
        for i, hint in enumerate(HINTS):
            hint_label_frame = HintLabelFrame(self.hint_frame, i, hint)
            hint_label_frame.grid(row=i+1, column=0, sticky='w')


if __name__ == "__main__":
    root = tk.Tk()
    LogicoApp(root).pack() # side="top", fill='both', expand=True
    root.mainloop()
