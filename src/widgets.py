import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


class SpinboxWithMemory(ttk.Spinbox):
    SPIN_MAX_VALUE = 5
    SPIN_MIN_VALUE = 2

    def __init__(self, parent: tk.Tk, *args, **kwargs):
        vcmd = (parent.register(self._validate_single_digit), '%P')
        super().__init__(
            *args,
            **kwargs,
            from_=self.SPIN_MIN_VALUE, 
            to=self.SPIN_MAX_VALUE,
            command=self._set_last_valid,
            validate='key',
            validatecommand=vcmd,
        )
        self.last_valid = kwargs.get('textvariable').get()
        self.min = kwargs.get('from_', self.SPIN_MIN_VALUE)
        self.max = kwargs.get('to', self.SPIN_MAX_VALUE)
        self.bind('<FocusOut>', self._on_focus_out)

    def _validate_single_digit(self, value: str):
        if value:
            return value.isdigit() and 0 <= int(value) <= 10
        else:
            return True

    def _set_last_valid(self):
        self.last_valid = self.get()

    def _on_focus_out(self, event):
        if not self.get().isdigit() or not (self.min <= int(self.get()) <= self.max):
            self.set(self.last_valid)


class HintLabelFrame(ttk.Frame):
    def __init__(self, parent: tk.Frame, hint_index: int, hint_text: str):
        super().__init__(parent)
        hint_num_label = ttk.Label(self, text=f"{hint_index + 1}) ")
        hint_label = ttk.Label(self, text=hint_text, wraplength=200, font=('TkDefaultFont', 10, 'normal'))
        hint_num_label.pack(side="left")
        hint_label.pack(side="left")
        hint_num_label.bind('<Button-1>', lambda _, obj=hint_label: self.toggle_strike(obj))
        hint_label.bind('<Button-1>', lambda _, obj=hint_label: self.toggle_strike(obj))


    def toggle_strike(self, obj: ttk.Label):
        font_object = tkfont.Font(font=obj.cget("font"))
        if font_object.actual().get('overstrike'):
            obj.config(font=('TkDefaultFont', 10, 'normal'))
        else:
            obj.config(font=('TkDefaultFont', 10, 'overstrike'))
