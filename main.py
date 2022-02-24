from tkinter import *
from typing import Optional, List

from structures import *
from tir import *

from constantes import *


# Class for the simulation.
# It contains the canvas and all the elements needed.
class Simulation:
    canvas: Canvas
    target: Optional[Character]
    shooter: Optional[Character]
    shots: List[Tir]
    walls: List[Wall]
    mode: int  # Placement mode
    temp: Optional[Point]  # Temporary point for wall placement

    def __init__(self, screen: Canvas):
        self.canvas = screen
        self.target = None
        self.shooter = None
        self.shots = []
        self.walls = []
        self.mode = 0
        self.temp = None

    # Toggle mode between character placement and obstacle placement
    def switch_mode(self):
        self.mode = (self.mode + 1) % 2
        print("Mode placement" if self.mode == 0 else "Mode obstacle")

    def set_target(self, x: int, y: int):
        new = Character(Point(x, y), T_SIZE, T_COLOR)
        if not new.is_in(self.shooter) and not self.touches_wall(new):
            self.target = new
            self.update()

    def set_shooter(self, x: int, y: int):
        new = Character(Point(x, y), S_SIZE, S_COLOR)
        if not new.is_in(self.target) and not self.touches_wall(new):
            self.shooter = new
            self.update()

    def set_wall(self, x: int, y: int, step: int):
        if step == 0:
            self.temp = Point(x, y)
        if step == 1:
            new = Wall(self.temp, Point(x, y), W_COLOR)

            if not new.is_in(self.shooter) and not new.is_in(self.target) and new.surface() >= MIN_WALL_SURFACE:
                self.walls.append(new)
                self.update()

    def undo_wall(self):
        self.walls.pop()
        self.update()

    def touches_wall(self, char: Character):
        for wall in self.walls:
            if wall.is_in(char):
                return True

    # Redraw the whole canvas
    def update(self):
        self.canvas.delete("all")
        if self.target:
            self.target.draw(self.canvas)
        if self.shooter:
            self.shooter.draw(self.canvas)
        # for tir in self.tirs:
        #     tir.draw(self.screen)
        for wall in self.walls:
            wall.draw(self.canvas)

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
    window.bind("<Button-1>",
                lambda event: scene.set_target(event.x, event.y) if scene.mode == 0 else scene.set_wall(event.x,
                                                                                                        event.y, 0))
    # Right click places the shooter if possible
    window.bind("<Button-3>",
                lambda event: scene.set_shooter(event.x, event.y) if scene.mode == 0 else scene.undo_wall())

    window.bind("<ButtonRelease-1>", lambda event: scene.set_wall(event.x, event.y, 1) if scene.mode == 1 else None)


if __name__ == "__main__":
    scene = init()
    scene.canvas.mainloop()
