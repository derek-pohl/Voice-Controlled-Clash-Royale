import speech_recognition as sr
import pygetwindow as gw
import pyautogui
import google.generativeai as genai
from PIL import Image
import mss
import json
import time

import config

# --- 1. SETUP ---

# Configure the Gemini API client
try:
    genai.configure(api_key=config.GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini: {e}. Make sure your API key is set in the .env file.")
    exit()

# --- 2. CORE FUNCTIONS ---

def listen_for_command():
    """Listens for a voice command via microphone and returns the transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for your command...")
        recognizer.pause_threshold = 1.0
        recognizer.adjust_for_ambient_noise(source, duration=1)
        # By removing the timeout and phrase_time_limit, listen() will now wait
        # indefinitely for a command and record until you pause.
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: '{command}'")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def capture_game_window():
    """Captures a screenshot of the specified game window using the fast mss library."""
    try:
        # Find the window
        windows = gw.getWindowsWithTitle(config.GAME_WINDOW_TITLE)
        if not windows:
            print(f"Error: Window with title '{config.GAME_WINDOW_TITLE}' not found.")
            return None, None
        window = windows[0]

        # Activate the window to ensure it's on top
        if not window.isActive:
            try:
                window.activate()
                time.sleep(0.2)  # Give it time to activate
            except Exception:
                # Fails on some OS configurations, but pyautogui can still work if window is visible
                print("Could not activate window, proceeding anyway.")

        # Define the capture area
        monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}

        # Capture using mss
        with mss.mss() as sct:
            sct_img = sct.grab(monitor)
            # Convert to a PIL Image, which is compatible with Gemini
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return img, window

    except Exception as e:
        print(f"An error occurred while capturing the window: {e}")
        return None, None

def get_ai_action(command, image):
    """Sends the command and screenshot to Gemini and gets the action."""
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are an expert AI assistant for the game Clash Royale. Your task is to interpret a user's voice command and a game screenshot to determine the best action.

    **Game Context:**
    - The game board is a grid. The user's side is the bottom half, the enemy's is the top half.
    - The user has 4 cards available at the bottom of the screen, in slots 1, 2, 3, and 4 (from left to right).
    - The grid for the entire arena is {config.BOARD_COLS} columns wide and {config.BOARD_ROWS} rows tall. (0,0) is the top-left corner.

    **User's Command:**
    "{command}"

    **Your Task:**
    1.  First, provide your reasoning. Analyze the screenshot and the user's command to explain your strategy. What is the current game state? What is the best move and why?
    2.  Based on your reasoning, identify the card that best matches the user's command from the 4 available slots.
    3.  Determine the target location on the grid for that card.
    4.  Provide your response in a clean JSON format with four keys: "reasoning", "card_slot", "grid_x", and "grid_y".

    **JSON Output Format Example:**
    {{
      "reasoning": "The user wants to counter the prince with the skeleton army. The skeleton army is in card slot 3, and the prince is located at approximately grid (8, 15). This is a positive elixir trade.",
      "card_slot": 3,
      "grid_x": 8,
      "grid_y": 15
    }}

    Now, analyze the user's command and the attached image and provide the JSON output.
    """

    print("Sending request to Gemini...")
    try:
        response = model.generate_content([prompt, image])
        # Clean up the response to extract only the JSON part
        json_text = response.text.strip().lstrip("```json").rstrip("```").strip()
        print(f"Gemini Raw Response: {json_text}")
        action = json.loads(json_text)
        return action
    except Exception as e:
        print(f"Error calling Gemini API or parsing JSON: {e}")
        if 'response' in locals():
            print(f"Full response text was: {response.text}")
        return None

def execute_action(action, window):
    """Executes the action by clicking the card and the target location."""
    card_slot = action.get("card_slot")
    grid_x = action.get("grid_x")
    grid_y = action.get("grid_y")

    if None in [card_slot, grid_x, grid_y]:
        print(f"Invalid action received from AI: {action}")
        return

    # 1. Calculate card click coordinates (absolute screen position)
    card_rel_x, card_rel_y = config.CARD_SLOTS[card_slot]
    card_abs_x = window.left + int(window.width * card_rel_x)
    card_abs_y = window.top + int(window.height * card_rel_y)

    # 2. Calculate grid click coordinates (absolute screen position)
    # This uses the calibrated playable area from config to be more accurate.
    playable_area = config.PLAYABLE_AREA_REL
    playable_abs_x_start = window.left + int(window.width * playable_area["x_start"])
    playable_abs_y_start = window.top + int(window.height * playable_area["y_start"])
    playable_abs_width = int(window.width * playable_area["width"])
    playable_abs_height = int(window.height * playable_area["height"])

    tile_width = playable_abs_width / config.BOARD_COLS
    tile_height = playable_abs_height / config.BOARD_ROWS
    # We add 0.5 to click the center of the tile
    grid_abs_x = playable_abs_x_start + int((grid_x + 0.5) * tile_width)
    grid_abs_y = playable_abs_y_start + int((grid_y + 0.5) * tile_height)

    print("-" * 20)
    print(f"Executing Action: {action.get('reasoning', 'N/A')}")
    print(f"-> Clicking Card {card_slot} at ({card_abs_x}, {card_abs_y})")
    print(f"-> Clicking Grid ({grid_x}, {grid_y}) at ({grid_abs_x}, {grid_abs_y})")
    print("-" * 20)

    # 3. Perform the clicks using pyautogui
    pyautogui.moveTo(card_abs_x, card_abs_y, duration=0.15)
    pyautogui.click()
    time.sleep(0.2)  # Small delay between clicks
    pyautogui.moveTo(grid_abs_x, grid_abs_y, duration=0.15)
    pyautogui.click()

    print("Action executed.")


# --- 3. MAIN APPLICATION LOOP ---

def main():
    """Main loop to listen, capture, process, and act."""
    print("--- Voice Controlled Clash Royale Assistant ---")
    print("Say 'stop program' or 'exit program' to quit.")
    print("Make sure the game window is visible.")
    while True:
        command = listen_for_command()
        if command:
            if "stop program" in command or "exit program" in command:
                print("Exiting program.")
                break

            image, window = capture_game_window()
            if image and window:
                action = get_ai_action(command, image)
                if action:
                    execute_action(action, window)

        time.sleep(0.5) # A small delay to prevent accidental loops

if __name__ == "__main__":
    main()