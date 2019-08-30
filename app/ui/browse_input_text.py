from pathlib import Path
from tkinter import Frame, Widget, Entry, Button, Label
from tkinter.constants import LEFT, X, END
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename

from app import ui
from app.ui import LABEL_PADDING


class BrowseInputText(Frame):

    def __init__(self, master: Widget, name: str, browse_folder=False, save=False, file_types=list()):
        super().__init__(master)
        self._name = name
        self._browse_folder = browse_folder
        self._save = save
        self._file_types = file_types
        # Add label
        label = Label(self, text=name, width=LABEL_PADDING)
        label.pack(side=LEFT)
        # Add entry
        self._entry = Entry(self)
        self._entry.pack(side=LEFT, fill=X, expand=True)
        # Add button
        button = Button(self, text="\u2026", command=self._browse)
        button.pack(side=LEFT)

    def _browse(self):
        if self._browse_folder:
            filename = askdirectory(title=self._name, initialdir=ui.CURRENT_LOCATION)
        else:
            if self._save:
                filename = asksaveasfilename(title=self._name, initialdir=ui.CURRENT_LOCATION,
                                             filetypes=self._file_types)
            else:
                filename = askopenfilename(title=self._name, initialdir=ui.CURRENT_LOCATION, filetypes=self._file_types)
        if filename:
            # Replace entry
            self._entry.delete(0, END)
            self._entry.insert(0, filename)
            # save current location
            ui.CURRENT_LOCATION = Path(filename).parent.as_posix()

    @property
    def value(self):
        return self._entry.get()

    @value.setter
    def value(self, value):
        self._entry.delete(0, END)
        self._entry.insert(0, value)
