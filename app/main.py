from tkinter import Tk

from app.ui.application_ui import ApplicationUi

if __name__ == '__main__':
    root = Tk()
    root.minsize(width=800, height=600)
    app = ApplicationUi(root)
    root.mainloop()
