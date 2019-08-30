from tkinter import Tk

from app.ui.application_ui import ApplicationUi


def start_app():
    root = Tk()
    root.minsize(width=800, height=600)
    app = ApplicationUi(root)
    root.mainloop()


if __name__ == '__main__':
    start_app()
