import threading
from tkinter import Frame, Tk, N, LabelFrame, S, Button, RIGHT
from tkinter.constants import X, BOTH, TOP, INSERT, END
from tkinter.scrolledtext import ScrolledText

import sys
from reportlab.lib.units import inch

from app.packages import gerber2pdf
from app.ui import BUTTON_PADDING
from app.ui.browse_input_text import BrowseInputText
from app.ui.string_list import StringList


class ApplicationUi(Frame):
    NAME = "Assembly PDF Generator"
    VERSION = "1.0.0"

    def print(self, value: str):
        self._console.insert(INSERT, value)
        self._console.insert(INSERT, "\n")
        self._console.see(END)

    def __init__(self, master: Tk):
        super().__init__(master)
        self._root = master
        # Set initial title
        master.wm_title(self.NAME + " " + self.VERSION)
        # Pack
        self.pack(fill=BOTH, expand=True)
        # Create tool frame
        self._tool_frame = Frame(self)
        self._tool_frame.pack(side=TOP, fill=BOTH, expand=True)
        self._ui_frame = Frame(self._tool_frame)

        content_frame = Frame(self._ui_frame)
        content_frame.pack(anchor=N, fill=X, expand=True)
        # Define inputs
        input_frame = LabelFrame(content_frame, text="Inputs", padx=5, pady=5)
        input_frame.pack(fill=X, expand=True)
        # Add list input
        self._file_list = StringList(input_frame, "Gerber Files", StringList.ListType.FILE)
        self._file_list.pack(fill=BOTH, expand=True)
        # Define outputs
        output_frame = LabelFrame(content_frame, text="Outputs", padx=5, pady=5)
        output_frame.pack(fill=X, expand=True)
        # Add output file
        self._output_file = BrowseInputText(output_frame, "Output PDF File", save=True,
                                            file_types=[('pdf file', '.pdf')])
        self._output_file.pack(fill=X, expand=True)
        # Define action frame
        action_frame = LabelFrame(self._ui_frame, text="Actions", padx=5, pady=5)
        action_frame.pack(anchor=S, fill=X, expand=True)
        # Add generate Button
        button = Button(action_frame, text="Generate", width=BUTTON_PADDING, command=self._generate_pdf)
        button.pack(side=RIGHT)
        self._ui_frame.pack(fill=BOTH, expand=True)
        # Create console
        self._console = ScrolledText(self, height=10)
        self._console.pack(side=TOP, fill=X, expand=False)

    def _print(self, value: str):
        self._console.insert(INSERT, value)
        self._console.insert(INSERT, "\n")
        self._console.see(END)

    def _generate_pdf(self):
        process_thread = threading.Thread(target=self._generate_pdf_process, args=(self._file_list.get(),
                                                                                   self._output_file.value))
        process_thread.start()

    def _generate_pdf_process(self, gerber_files: list, output_file: str):
        self._print("Generating pdf...")
        # Setup gerber 2 PDF
        gerber2pdf.gerberScale = (0.99, 0.99)
        gerber2pdf.gerberPageSize = (17.0 * inch, 11.0 * inch)
        gerber2pdf.gerberOutputFile = output_file
        # Execute translation
        success = True
        try:
            gerber2pdf.Translate(gerber_files)
        except:
            success = False
            self._print("GERBER2PDF ERROR: " + sys.exc_info()[0])
        if success:
            self._print("Success!")
