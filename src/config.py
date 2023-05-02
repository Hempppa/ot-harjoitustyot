import os
from dotenv import load_dotenv

"""Täällä ladataan tiedostojen nimet .env tiedostosta
"""

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE") or "background.png"
FLAG_IMAGE = os.getenv("FLAG_IMAGE") or "flag.png"
HIGHLIGHT_IMAGE = os.getenv("HIGHLIGHT_IMAGE") or "highlight.png"
COVER_IMAGE = os.getenv("COVER_IMAGE") or "tile.png"
TILE_0 = os.getenv("TILE_0") or "tile0.png"
TILE_1 = os.getenv("TILE_1") or "tile1.png"
TILE_2 = os.getenv("TILE_2") or "tile2.png"
TILE_3 = os.getenv("TILE_3") or "tile3.png"
TILE_4 = os.getenv("TILE_4") or "tile4.png"
TILE_5 = os.getenv("TILE_5") or "tile5.png"
TILE_6 = os.getenv("TILE_6") or "tile6.png"
TILE_7 = os.getenv("TILE_7") or "tile7.png"
TILE_8 = os.getenv("TILE_8") or "tile8.png"
MINE_IMAGE = os.getenv("MINE_IMAGE") or "tile9.png"
LEADERBOARD_REPO = os.getenv("LEADERBOARD_REPO") or "leaderboard.db"
