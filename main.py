import time
from tkinter import *

from bar import Infos
from shot import *
from structures import *


# Class for the simulation.
# It contains the canvas and all the elements needed.
class Simulation:
    screen: Canvas
    bar: Infos

    target: Optional[Character]
    shooter: Optional[Character]
    shots: List[Shot]
    walls: List[Wall]
    mode: int  # Placement mode

    temp: Optional[Point]  # Temporary point for wall placement
    preview: Optional[Wall]  # Wall preview

    def __init__(self, screen: Canvas, bar: Infos):
        self.screen = screen
        self.bar = bar
        self.target = None
        self.shooter = None
        self.walls = []
        self.shots = []
        self.mode = 0

        self.temp = None
        self.preview = None

    # Toggle mode between character placement and wall placement
    def switch_mode(self):
        if self.mode == 1:
            self.clear_preview()
        self.mode = (self.mode + 1) % 2
        self.bar.change_text(self.mode)

    def set_target(self, x: int, y: int):
        new = Character(Point(x, y), settings["T_SIZE"], settings["T_COLOR"])
        if not new.is_in(self.shooter) and not self.touches_wall(new):
            self.target = new
            self.update()

    def set_shooter(self, x: int, y: int):
        new = Character(Point(x, y), settings['S_SIZE'], settings['S_COLOR'])
        if not new.is_in(self.target) and not self.touches_wall(new):
            self.shooter = new
            self.update()

    def set_wall(self, x: int, y: int, release: bool = False):
        if not release and self.temp is None:
            self.temp = Point(x, y)
        elif release and self.temp is not None:
            new = Wall(self.temp, Point(x, y), settings['W_COLOR'])

            if not new.is_in(self.shooter) and not new.is_in(self.target) \
                    and new.surface() >= settings['MIN_WALL_SURFACE']:
                self.walls.append(new)
                self.clear_preview()

    def undo_wall(self):
        if self.temp:
            self.clear_preview()
            return

        if len(self.walls) > 0:
            self.walls.pop()
            self.update()

    def wall_preview(self, x, y):
        if self.temp is not None:
            self.update()
            self.preview = Wall(self.temp, Point(x, y), settings['PREVIEW_COLOR'])
            self.preview.draw(self.screen, True)

    def clear_preview(self):
        self.temp = None
        self.preview = None
        self.update()

    def touches_wall(self, char: Character):
        for wall in self.walls:
            if wall.is_in(char):
                return True

    # Redraw the whole canvas
    def update(self, erase=True):
        if erase:
            self.screen.delete("all")

        if self.target:
            self.target.draw(self.screen)
        if self.shooter:
            self.shooter.draw(self.screen)
        for wall in self.walls:
            wall.draw(self.screen)

    # Start the simulation
    def run(self):
        if self.target and self.shooter:
            self.update()
            self.shots.clear()
            print("\n\nLet's go !")
            print(
                f"The shooter and the target are {round(self.target.pos.distance(self.shooter.pos) - self.shooter.radius - self.target.radius, 2)} units apart")

            N = 360 * settings['PRECISION']
            start = time.time()
            fastest = None
            for angle in range(0, N):
                shot = Shot(self.shooter.pos, (360 * angle) / N)
                touch = shot.shoot(self.target, self.shooter, self.walls)
                if touch:
                    if not fastest:
                        fastest = touch
                    elif touch.length < fastest.length:
                        self.shots.append(fastest)
                        fastest = touch
                    else:
                        self.shots.append(touch)

            total = round(time.time() - start, 2)
            print(f"Done in {total} second{'' if total <= 2 else 's'}")

            nb = len(self.shots) + 1 if fastest else 0
            if nb == 0:
                print(f"No shot hit")
            elif nb == 1:
                points = len(fastest.path)
                print(f"Only one shot hit ({points - 2} ricochet{'' if points <= 3 else 's'})")
            else:
                print(f"{nb} shots got to the target")

            for shot in self.shots:
                shot.draw(self.screen)

            if fastest:
                fastest.draw(self.screen, settings["FASTEST_COLOR"])
                if nb != 1:
                    points = len(fastest.path)
                    print(
                        f"Best shot did {points - 2} ricochet{'' if points <= 3 else 's'} and traveled {round(fastest.length - self.shooter.radius, 2)} units")

            self.update(erase=False)


# Initialization of the window and the events handler
def init() -> Simulation:
    window = Tk()
    window.title(settings["TITLE"])
    window.resizable(False, False)
    window.configure(background=settings["BAR_COLOR"])

    x = int((window.winfo_screenwidth() / 2) - (settings['WIDTH'] / 2))
    y = int((window.winfo_screenheight() / 2) - (settings['HEIGHT'] * 1.35 / 2))
    window.geometry(f"{settings['WIDTH']}x{int(settings['HEIGHT'] * 1.35)}+{x}+{y}")

    canvas = Canvas(window, width=settings['WIDTH'], height=settings['HEIGHT'], background=settings['BG_COLOR'], bd=0)
    canvas.grid(row=0)

    bar = Frame(window, background=settings['BAR_COLOR'], bd=0)
    bar.grid(row=1, sticky="nsew")

    bar.grid_columnconfigure(0, weight=1)
    bar.grid_columnconfigure(1, weight=0)
    bar.grid_columnconfigure(2, weight=1)

    infos = Infos(bar, settings['BAR_COLOR'])

    window.update()

    events_handler(window, canvas)
    return Simulation(canvas, infos)


def events_handler(window: Tk, canvas: Canvas):
    # Keyboard events :
    # Pressing <Return> switch the placement mode
    window.bind("<Return>", lambda event: scene.switch_mode())
    # Pressing <space> start the simulation
    window.bind("<space>", lambda event: scene.run())
    window.bind("<Escape>", lambda event: scene.clear_preview())

    # Mouse events in the canvas:
    # Left click places the target if possible | Start putting a wall
    canvas.bind("<ButtonPress-1>",
                lambda event: scene.set_target(event.x, event.y) if scene.mode == 0 else scene.set_wall(event.x,
                                                                                                        event.y))
    # Right click places the shooter if possible | Remove last wall
    canvas.bind("<ButtonPress-3>",
                lambda event: scene.set_shooter(event.x, event.y) if scene.mode == 0 else scene.undo_wall())
    # Release left click put a wall if possible
    canvas.bind("<ButtonRelease-1>",
                lambda event: scene.set_wall(event.x, event.y, True) if scene.mode == 1 else None)

    # Show the future wall
    canvas.bind("<Motion>", lambda event: scene.wall_preview(event.x, event.y) if scene.mode == 1 else None)


# You can change the constants in constats.py to have fun
if __name__ == "__main__":
    scene = init()
    scene.screen.mainloop()
