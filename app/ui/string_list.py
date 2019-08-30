from enum import Enum
from tkinter import Frame, Widget, Label, Button, Listbox, Scrollbar
from tkinter.constants import LEFT, BOTH, X, RIGHT, VERTICAL, END, Y, HORIZONTAL
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter.simpledialog import askstring

from pathlib import Path

from app import ui
from app.ui import LABEL_PADDING


class StringList(Frame):

    class ListType(Enum):
        STRING = 0
        FILE = 1
        DIRECTORY = 2

    def __init__(self, master: Widget, name: str, list_type: ListType):
        super().__init__(master)
        self._list_type = list_type
        self._name = name
        # Set minimum size
        # Add label
        label = Label(self, text=name, width=LABEL_PADDING)
        label.pack(side=LEFT)
        # Add frame for controls
        controls_frame = Frame(self)
        controls_frame.pack(side=LEFT, fill=X, expand=True)
        # Add frame for buttons
        buttons_frame = Frame(controls_frame)
        buttons_frame.pack(fill=X, expand=True)
        # Add the plus button
        plus_button = Button(buttons_frame, text="\u2795", command=self._add)
        plus_button.pack(side=RIGHT)
        # Add the remove button
        remove_button = Button(buttons_frame, text="\u2716", command=self._remove)
        remove_button.pack(side=RIGHT)
        # Add the down button
        down_button = Button(buttons_frame, text="\u25BC", command=self._down)
        down_button.pack(side=RIGHT)
        # Add the up button
        up_button = Button(buttons_frame, text="\u25B2", command=self._up)
        up_button.pack(side=RIGHT)
        # Add list frame
        list_frame = Frame(controls_frame)
        list_frame.pack(fill=BOTH, expand=True)
        # Add list
        self._list = Listbox(list_frame, height=15)
        self._list.pack(side=LEFT, fill=BOTH, expand=True)
        # Add vertical scrollbar
        vscroll = Scrollbar(list_frame, orient=VERTICAL)
        vscroll.pack(side=RIGHT, fill=Y)
        self._list.config(yscrollcommand=vscroll.set)
        vscroll.config(command=self._list.yview)
        # Add horizontal scrollbar
        hscroll = Scrollbar(controls_frame, orient=HORIZONTAL)
        hscroll.pack(fill=X, expand=True)
        self._list.config(xscrollcommand=hscroll.set)
        hscroll.config(command=self._list.xview)

    def _add(self):
        if self._list_type == self.ListType.STRING:
            values = list(askstring(self._name, "Value"))
        elif self._list_type == self.ListType.FILE:
            values = askopenfilenames(title=self._name, initialdir=ui.CURRENT_LOCATION)
            # save current location
            if values:
                ui.CURRENT_LOCATION = Path(values[0]).parent.as_posix()
        else:
            values = list(askdirectory(title=self._name, initialdir=ui.CURRENT_LOCATION))
            # save current location
            if values:
                ui.CURRENT_LOCATION = Path(values[0]).parent.as_posix()
        # Add value
        if values:
            for value in values:
                self._list.insert(END, value)

    def add(self, values: list):
        if values:
            for value in values:
                self._list.insert(END, value)

    def _remove(self):
        if self._list.curselection():
            # Save selection for next selection
            current_selection = self._list.curselection()[0]
            # Remove item
            self._list.delete(self._list.curselection()[0])
            # Reselect an item if possible
            if self._list.size():
                if current_selection > self._list.size() - 1:
                    current_selection -= 1
                self._list.select_set(current_selection)

    def _down(self):
        if self._list.curselection():
            if self._list.curselection()[0] >= self._list.size() - 1:
                return
            # Insert at index + 2 (after next item)
            self._list.insert(self._list.curselection()[0] + 2, self._list.get(self._list.curselection()[0]))
            # Set next selection
            next_selection = self._list.curselection()[0] + 1
            # Remove
            self._list.delete(self._list.curselection()[0])
            # Select item
            self._list.selection_set(next_selection)

    def _up(self):
        if self._list.curselection():
            if self._list.curselection()[0] <= 0:
                return
            # Set next selection
            next_selection = self._list.curselection()[0] - 1
            # Insert at index - 1
            self._list.insert(self._list.curselection()[0] - 1, self._list.get(self._list.curselection()[0]))
            # Remove
            self._list.delete(self._list.curselection()[0])
            # Select item
            self._list.selection_set(next_selection)

    def get(self):
        return list(self._list.get(0, END))
