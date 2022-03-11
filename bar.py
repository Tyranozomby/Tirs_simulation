from tkinter import Frame, Label, Scale

from settings.settings import settings


class Infos:
    bar: Frame
    color: str

    mode: Label
    mode_text = ["Placing characters", "Placing obstacles"]

    def __init__(self, bar: Frame, color: str):
        self.bar = bar
        self.color = color
        self.show_settings()

    def show_settings(self):
        title = Label(self.bar, text="Settings", font="verdana 16 bold underline", background=self.color)
        title.grid(row=0, column=0, columnspan=3)

        # Col 0
        Label(self.bar, text="Characters", font="verdana 12", background=self.color).grid(row=1, column=0)
        G1 = Frame(self.bar, bg=self.color, highlightbackground="#00AAF8", highlightthickness=2, pady=2)
        G1.grid(row=2, column=0, sticky="ns")

        # Col 1
        self.mode = Label(self.bar, text=self.mode_text[0], font="verdana 15 bold", background=self.color)
        self.mode.grid(row=1, column=1, rowspan=2)

        # Col 2
        Label(self.bar, text="Shots", font="verdana 12", background=self.color).grid(row=1, column=2)
        G2 = Frame(self.bar, bg=self.color, highlightbackground="#00AAF8", highlightthickness=2, pady=2)
        G2.grid(row=2, column=2)

        # G1
        t_size = Label(G1, text=f"Target's size :", font="verdana 10 underline",
                       background=self.color)
        t_size.grid(row=0)

        t_size_controller = Scale(G1, orient="horizontal", from_=5, to=50, sliderlength=20, resolution=5,
                                  bg=self.color,
                                  bd=0, highlightthickness=0, command=settings.change_T_SIZE)
        t_size_controller.set(settings['T_SIZE'])
        t_size_controller.grid(row=1)

        s_size = Label(G1, text=f"Shooter's size :", font="verdana 10 underline",
                       background=self.color)
        s_size.grid(row=2)

        s_size_controller = Scale(G1, orient="horizontal", from_=5, to=50, sliderlength=20, resolution=5,
                                  bg=self.color,
                                  bd=0, highlightthickness=0, command=settings.change_S_SIZE)
        s_size_controller.set(settings['S_SIZE'])
        s_size_controller.grid(row=3)

        # G2
        precision = Label(G2, text=f"Precision :", font="verdana 10 underline",
                          background=self.color)
        precision.grid(row=0)

        precision_controller = Scale(G2, orient="horizontal", from_=1, to=5, sliderlength=20, resolution=1,
                                     bg=self.color,
                                     bd=0, highlightthickness=0, command=settings.change_PRECISION)
        precision_controller.set(settings['PRECISION'])
        precision_controller.grid(row=1)

        bounces = Label(G2, text=f"Max ricochets :", font="verdana 10 underline",
                        background=self.color)
        bounces.grid(row=2)

        bounces_controller = Scale(G2, orient="horizontal", from_=0, to=50, sliderlength=20, resolution=1,
                                   bg=self.color,
                                   bd=0, highlightthickness=0, command=settings.change_BOUNCES)
        bounces_controller.set(settings['MAX_BOUNCES'])
        bounces_controller.grid(row=3)

    def change_text(self, mode: int):
        self.mode["text"] = self.mode_text[mode]
