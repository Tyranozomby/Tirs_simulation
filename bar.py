from tkinter import Frame, Label

from constantes import WIDTH, HEIGHT


class Infos:
    bar: Frame
    color: str

    mode: Label
    left_click: Label
    right_click: Label
    enter: Label
    space: Label

    title = ["Placing characters", "Placing walls"]
    left = ["Place the target", "Hold and drag to place a wall"]
    right = ["Place the shooter", "Remove last wall"]

    def __init__(self, bar: Frame, color: str):
        bar.configure(background=color)

        self.mode = Label(text=self.title[0], bg=color, font="verdana 15 bold")
        self.mode.place(x=WIDTH * .4, y=HEIGHT * 1.01)

        Label(text="Left Click :", bg=color, font="verdana 12 underline bold").place(x=WIDTH * .1, y=HEIGHT * 1.065)
        self.left_click = Label(text=self.left[0], bg=color, font="verdana 12")
        self.left_click.place(x=WIDTH * .2, y=HEIGHT * 1.065)

        Label(text="Right Click :", bg=color, font="verdana 12 underline bold").place(x=WIDTH * .1, y=HEIGHT * 1.14)
        self.right_click = Label(text=self.right[0], bg=color, font="verdana 12")
        self.right_click.place(x=WIDTH * .21, y=HEIGHT * 1.14)

        Label(text="Return Button :", bg=color, font="verdana 12 underline bold").place(x=WIDTH * .5, y=HEIGHT * 1.065)
        self.enter = Label(text="Press to switch to wall placement", bg=color, font="verdana 12")
        self.enter.place(x=WIDTH * .65, y=HEIGHT * 1.065)

        Label(text="Space Bar :", bg=color, font="verdana 12 underline bold").place(x=WIDTH * .5, y=HEIGHT * 1.14)
        self.space = Label(text="Press to START the simulation", bg=color, font="verdana 12")
        self.space.place(x=WIDTH * .61, y=HEIGHT * 1.14)

        self.bar = bar

    def change_text(self, mode: int):
        self.mode.configure(text=self.title[mode])
        self.left_click.configure(text=self.left[mode])
        self.right_click.configure(text=self.right[mode])
