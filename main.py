from tkinter import *
from typing import Optional, List

from structures import *
from tir import *

from constantes import *


# Class for the simulation.
# It contains the canvas and all the elements needed.
class Simulation:
    canvas: Canvas
    target: Optional[Circle]
    shooter: Optional[Circle]
    shots: List[Tir]
    walls: List[Rectangle]
    mode: int

    def __init__(self, screen: Canvas):
        self.canvas = screen
        self.target = None
        self.shooter = None
        self.shots = []
        self.walls = []
        self.mode = 0

    # Toggle mode between character placement and obstacle placement
    def switch_mode(self):
        self.mode = (self.mode + 1) % 2
        print("Mode placement" if self.mode == 0 else "Mode obstacle")

    def set_target(self, x, y):
        print("clic")
        new = Circle(Point(x, y), T_SIZE, T_COLOR)
        if not self.shooter or not new.is_in(self.shooter):
            self.target = new
            self.update()

    def set_shooter(self, x, y):
        new = Circle(Point(x, y), S_SIZE, S_COLOR)
        if not self.target or not new.is_in(self.target):
            self.shooter = new
            self.update()

    # Redraw the whole canvas
    def update(self):
        self.canvas.delete("all")
        if self.target:
            self.target.draw(self.canvas)
        if self.shooter:
            self.shooter.draw(self.canvas)
        # for tir in self.tirs:
        #     tir.draw(self.screen)
        # for mur in self.murs:
        #     mur.draw(self.screen)

    # Start the simulation
    def run(self):
        print("Let's go")
        if self.target and self.shooter:
            for angle in range(0, 360 * PRECISION):
                pass
        self.update()


# Initialization of the window and the events handler
def init() -> Simulation:
    window = Tk(TITLE)
    screen = Canvas(window, width=WIDTH, height=HEIGHT)
    screen.pack()
    screen.configure(background=BG_COLOR)

    x = int((screen.winfo_screenwidth() / 2) - (WIDTH / 2))
    y = int((screen.winfo_screenheight() / 2) - (HEIGHT / 2))

    window.resizable(False, False)
    window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    screen.update()

    events_handler(window)
    return Simulation(screen)


def events_handler(window: Tk):
    # Keyboard events :
    # Pressing <Return> switch the placement mode
    window.bind("<Return>", lambda event: scene.switch_mode())
    # Pressing <space> start the simulation
    window.bind("<space>", lambda event: scene.run())

    # Mouse events :
    # Left click places the target if possible
    window.bind("<Button-1>", lambda event: scene.set_target(event.x, event.y))
    # Right click places the shooter if possible
    window.bind("<Button-3>", lambda event: scene.set_shooter(event.x, event.y))


if __name__ == "__main__":
    scene = init()
    scene.canvas.mainloop()
