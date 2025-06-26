import os
from dotenv import load_dotenv

load_dotenv()

# --- Gemini AI Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Game Configuration ---
# IMPORTANT: Change this to the exact title of your game window.
# You can find it in the top bar of the Google Play Games window when Clash Royale is running.
GAME_WINDOW_TITLE = "Clash Royale"

# The grid system you described.
# The entire arena is 18 columns wide and 28 rows tall (14 for each side).
BOARD_ROWS = 28
BOARD_COLS = 18

# --- IMPORTANT CALIBRATION ---
# These are the RELATIVE positions (from 0.0 to 1.0) of the center of your 4 cards.
# You will need to adjust these for your screen resolution and window size.
# (0.0, 0.0) is the top-left corner of the window.
# (1.0, 1.0) is the bottom-right corner.
# Calculated from an 828x1374 window based on your image map.
CARD_SLOTS = {
    1: (0.3792, 0.8934),  # Card 1
    2: (0.5501, 0.8926),  # Card 2
    3: (0.7162, 0.8941),  # Card 3
    4: (0.8919, 0.8890),  # Card 4
}

# These are the RELATIVE coordinates of the playable game grid within the window.
# This ensures that clicks are placed correctly on the grid, not just the window.
# Calculated from an 828x1374 window based on your image map.
PLAYABLE_AREA_REL = {
    "x_start": 0.1546,  # 128px from left
    "y_start": 0.1215,  # 167px from top
    "width":   0.7838,  # Spans 649px
    "height":  0.6354,  # Spans 873px
}