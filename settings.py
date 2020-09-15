# Image
MOB_UP_IMG = "rockSnowDown.png"
MOB_DOWN_IMG = "rockSnow.png"
GROUND_IMG = "groundSnow.png"
NUMBERS = [(432, 1743, 53, 78), (512, 1093, 37, 76), (477, 1350, 51, 77),
           (485, 1679, 51, 78), (432, 1537, 55, 76), (485, 1823, 50, 76),
           (432, 1885, 53, 77), (478, 1173, 51, 76), (461, 899, 51, 78), (458, 1962, 53, 77)]

# game options/settings
TITLE = "Tappy Plane"
WIDTH = 800
HEIGHT = 600
FPS = 60
FONT_NAME = 'comicsansms'
HS_FILE = "highscore.txt"
SPRITESHEET = ["sheet.png"]

# Player properties
PLAYER_GRAV = 0.5 #0.8
PLAYER_JUMP = 5
PLAYER_DISP = 5

# Game properties
BOOST_POWER = 15
POW_SPAWN_PCT = 7 
PLAYER_LAYER = 2
PUFF_LAYER = 2
GROUND_LAYER = 2
POW_LAYER = 2
MOB_LAYER = 1
CLOUD_LAYER = 0

# Starting mobs
MOB_UP_LIST = [(250,0), (500,0), (750,0)]
MOB_DOWN_LIST = [(270,HEIGHT), (480,HEIGHT), (750,HEIGHT)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
GOLDEN = (255, 204, 0)
SILVER_CLR = (171, 171, 171)
BRONZE_CLR = (215, 98, 65)
SPL_RED = (200, 62, 62)
BGCOLOR = LIGHTBLUE
