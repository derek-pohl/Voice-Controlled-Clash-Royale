# Voice-Controlled Clash Royale

A Python application that allows you to control Clash Royale on Windows using voice commands and AI. Simply speak your commands, and the AI will analyze the game state and execute the optimal moves for you.

Eg, "Place the cannon to defend the hog rider" or "Fireball the left princess tower"

## How It Works

1. **Listen**: The application continuously listens for your voice commands (with Google Speech Recognition) through your microphone
2. **Capture**: Takes a screenshot of the Clash Royale game window
3. **Analyze**: Sends both your command and the screenshot to Gemini AI for analysis
4. **Execute**: Automatically clicks the appropriate card and target location on the game board

## Prerequisites

- Python 3.7 or higher
- A Google Gemini API key, which can be found at [Google AI Studio](aistudio.google.com) for free
- Clash Royale running on your computer [via Google Play Games for Windows](https://play.google.com/googleplaygames/)
- A working microphone for voice input. It has to be a good-ish microphone.

## Installation

1. **Clone the repository** (or download):
   ```bash
   git clone https://github.com/yourusername/Voice-Controlled-Clash-Royale.git
   cd Voice-Controlled-Clash-Royale
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**:
   - Get a free API key from [Google AI Studio](aistudio.google.com)
   - Create a `.env` file in the project directory
   - Add your API key:
     ```
     GEMINI_API_KEY="your_api_key_here"
     ```

4. **Configure the game window (likely NOT needed)**:
   - Open `config.py`
   - Update `GAME_WINDOW_TITLE` to match your Clash Royale window title exactly.
   - Adjust `CARD_SLOTS` and `PLAYABLE_AREA_REL` if needed for your screen resolution

## Usage

1. **Start Clash Royale** on your computer and make sure it's visible on screen

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Grant permissions** when prompted for microphone access

4. **Start playing**:
   - The application will listen for your voice commands
   - Say things like:
     - "Deploy skeleton army at the left bridge"
     - "Place fireball on the tower"
     - "Counter the giant with inferno tower"
     - "Defend with knight"
   - The AI will analyze the game state and execute the best move

5. **Stop the program**:
   - Say "stop program" or "exit program" to quit

## Configuration

### AI Model Selection
You can change the Gemini model in `config.py`:
- `gemini-2.5-flash-lite-preview-06-17` (default) - Faster, lighter
- `gemini-2.5-flash` - Slower but wayyy more intelligent

## Troubleshooting

### Common Issues

**"Window not found" error**:
- Make sure Clash Royale is running and visible
- Check that `GAME_WINDOW_TITLE` in `config.py` matches exactly
- Try minimizing and maximizing the game window

**Voice recognition not working**:
- Check your microphone permissions
- Ensure your microphone is set as the default recording device
- Try speaking more clearly or adjusting microphone volume

**API errors**:
- Verify your Gemini API key is correct in the `.env` file
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**Clicking in wrong positions**:
- The card slots and playable area coordinates may need calibration for your screen resolution
- Adjust `CARD_SLOTS` and `PLAYABLE_AREA_REL` values in `config.py`

### Calibration

If clicks are landing in the wrong positions, you may need to recalibrate:

1. **Card Positions**: Update `CARD_SLOTS` with relative coordinates (0.0-1.0) of your card slots
2. **Playable Area**: Adjust `PLAYABLE_AREA_REL` to match the game board boundaries on your screen

## File Structure

```
Voice-Controlled-Clash-Royale/
├── main.py              # Main application logic
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env                # API keys (create this file)
└── README.md           # This file (hi)
```

## Dependencies

- `google-generativeai` - Google Gemini AI integration
- `speechrecognition` - Voice command recognition
- `pyaudio` - Audio input handling
- `pygetwindow` - Window management
- `pyautogui` - Mouse automation
- `python-dotenv` - Environment variable management
- `mss` - Fast screenshot capture
- `Pillow` - Image processing