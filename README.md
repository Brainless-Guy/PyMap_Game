# PyMap  Game

## Overview

This application, built using `customtkinter` and `tkinter`, allows users to load a map, mark coordinates, save them as presets, and play a game by guessing locations on the map. The application provides interactive elements like buttons, dialogs, and a toggle for dark mode.

---

## Features

### 1. **Load Map and Record Places**

- The **Load Map** button allows users to select an image file (PNG, JPG, or JPEG) to use as a map.
- Clicking on the map lets users mark coordinates with a name, storing them in a list.

### 2. **Create and Save Presets**

- After recording places, users can save them as a preset.
- Presets are stored in a `presets.json` file for future use.
- The **Upload Preset** button allows importing presets from external files.

### 3. **Play the Game**

- The **Play** button starts a game using saved presets.
- Players guess locations by clicking on the map based on given place names.
- Coordinates and guesses are recorded in a `stored_score.txt` file.

### 4. **Dark Mode Toggle**

- A switch button toggles between dark and light modes.

### 5. **Custom Silent MessageBox**

- A custom `SilentMessageBox` replaces default dialogs with non-sound popups.

---

## Important Components

### `Map Game App`

The main class managing the game logic and user interactions.

- **Buttons and Controls**:

  - Load Map, Play, Reset, Upload Preset, Dark Mode Toggle, and Quit.

- **Methods**:

  - `load_map()`: Loads and displays the map.
  - `record_coordinates(event)`: Records coordinates when a user clicks.
  - `play_game()`: Starts the game using saved presets.
  - `toggle_dark_mode()`: Toggles between light and dark modes.
  - `save_presets() / load_presets()`: Handles preset storage.

- **SilentMessageBox**:

  - Custom `showinfo` method displays dialogs without sound.

### Game Rounds

- **start\_round()**: Displays a place name to find on the map.
- **get\_user\_guess()**: Waits for the user's guess.
- **show\_results()**: Shows the comparison between the guess and actual location.

---

## How to Run
### INSTALL PYTHON FIRST
1. Ensure `customtkinter` and `PIL` are installed.Open CMD and Enter This
  ```
  pip install -r requirements.txt 
  ```

2. Place `presets.json` (if available) in the same directory.
3. Run the script:
   ```
   python map.py
   ```

# Virus?
  - check the file here: [virustotal](https://www.virustotal.com/gui/file/b0b305a4a6eeed06975c36830793dc19b64612cde04a5b6a4706c686135b72e7)


