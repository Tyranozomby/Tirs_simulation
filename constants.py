# This file regroups all the constants useful for this project

TITLE: str = "Simulation de tirs"  # Window's title
WIDTH: int = 1000  # Window's width
HEIGHT: int = 700  # Window's height

BG_COLOR: str = "cyan"  # Default background color
BAR_COLOR: str = "white"  # Bar background color

PRECISION: int = 2  # Number of shot per degree, the more, the laggier (More than 5 isn't useful)
MAX_BOUNCES: int = 20  # Number of bounces allowed for a shot
L_COLOR: str = "#FF7F00"  # Shot line's color

T_SIZE: int = 25  # Radius of the circle
T_COLOR: str = "blue"  # Target's color

S_SIZE: int = 25  # Radius of the circle
S_COLOR: str = "red"  # Shooter's color

W_COLOR: str = "black"  # Wall's color
WP_COLOR: str = "gray50"  # Wall preview color
MIN_WALL_SURFACE: int = 1000  # Minimal wall surface allowed
