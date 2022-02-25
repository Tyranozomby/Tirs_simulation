from tkinter import *
from typing import Optional, List

from structures import *
from shot import *

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
    preview: Optional[Wall]  # Wall preview

    def __init__(self, screen: Canvas):
        self.canvas = screen
        self.target = None
        self.shooter = None
        self.walls = []
        self.shots = []
        self.mode = 0

        self.temp = None
        self.preview = None

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

    def set_wall(self, x: int, y: int, release: bool = False):
        if not release and self.temp is None:
            self.temp = Point(x, y)
        elif release and self.temp is not None:
            new = Wall(self.temp, Point(x, y), W_COLOR)

            if not new.is_in(self.shooter) and not new.is_in(self.target) and new.surface() >= MIN_WALL_SURFACE:
                self.walls.append(new)
                self.clear_preview()

    def undo_wall(self):
        if len(self.walls) > 0:
            self.walls.pop()
            self.update()

    def wall_preview(self, x, y):
        if self.temp is not None:
            self.update()
            self.preview = Wall(self.temp, Point(x, y), WP_COLOR)
            self.preview.draw(self.canvas, True)

    def clear_preview(self):
        self.temp = None
        self.preview = None
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
    window.bind("<Escape>", lambda event: scene.clear_preview())

    # Mouse events :
    # Left click places the target if possible | Start putting a wall
    window.bind("<ButtonPress-1>",
                lambda event: scene.set_target(event.x, event.y) if scene.mode == 0 else scene.set_wall(event.x,
                                                                                                        event.y))
    # Right click places the shooter if possible | Remove last wall
    window.bind("<Button-3>",
                lambda event: scene.set_shooter(event.x, event.y) if scene.mode == 0 else scene.undo_wall())
    # Release left click put a wall if possible
    window.bind("<ButtonRelease-1>",
                lambda event: scene.set_wall(event.x, event.y, True) if scene.mode == 1 else None)

    # Show the future wall
    window.bind("<Motion>", lambda event: scene.wall_preview(event.x, event.y))


if __name__ == "__main__":
    scene = init()
    scene.canvas.mainloop()
