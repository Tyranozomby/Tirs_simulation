from tkinter import *
from typing import Optional, List

from structures import *
from tir import *

TITRE: str = "Simulation de tirs"
WIDTH: int = 1000
HEIGHT: int = 700

PRECISION: int = 1


class Scene:
    screen: Tk
    target: Optional[Cercle]
    shooter: Optional[Cercle]
    tirs: List[Tir]
    murs: List[Rectangle]
    temp_point: Optional[Point]
    mode: int

    def __init__(self, screen: Tk):
        self.debug = []
        self.screen = screen
        self.target = None
        self.shooter = None
        self.tirs = []
        self.murs = []
        self.temp_point = None
        self.mode = 0

    def switch_mode(self):
        self.mode = (self.mode + 1) % 2
        print("Mode placement" if self.mode == 0 else "Mode obstacle")

    def update(self):
        pass
        # if self.target:
        #     self.target.draw(self.screen)
        # if self.shooter:
        #     self.shooter.draw(self.screen)
        # for tir in self.tirs:
        #     tir.draw(self.screen)
        # for mur in self.murs:
        #     mur.draw(self.screen)

    def run(self):
        print("Let's go")
        if self.target and self.shooter:
            for angle in range(0, 360 * PRECISION):
                pass  # TODO


def init() -> Scene:
    screen = Tk(TITRE)

    x = int((screen.winfo_screenwidth() / 2) - (WIDTH / 2))
    y = int((screen.winfo_screenheight() / 2) - (HEIGHT / 2))

    screen.resizable(False, False)
    screen.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    screen.update()

    return Scene(screen)


def event_handler():
    scene.screen.bind("<Return>", lambda event: scene.switch_mode())
    scene.screen.bind("<space>", lambda event: scene.run())


def start():
    event_handler()

    scene.screen.mainloop()


if __name__ == "__main__":
    scene = init()
    start()
