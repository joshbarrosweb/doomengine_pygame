# Doom Engine with Pygame

This project is a recreation of the classic DOOM game, implemented in Python using the Pygame library.

## Special Thanks

Special thanks to id Software, the creators of the original DOOM, for inspiring this project!
And also Stanislav Petrov (CoderSpace on YouTube) for originally creating this amazing PyGame version of Doom Engine!

- [CoderSpace's Doom Engine Playlist](https://www.youtube.com/playlist?list=PLi77irUVkDasNAYQPr3N8nVcJLQAlANva)
- [CoderSpace GitHub](https://github.com/StanislavPetrovV)

## Project Structure

The project has the following file and folder structure:

### `src`

This folder contains the source code files for the game:

- `main.py`: The main entry point of the game. It sets up the game loop and initiates the other modules of the game.
- `asset_data.py`: Contains the AssetData class which handles the processing and organization of DOOM's binary asset data, such as textures, sprites, and audio files.
- `bsp.py`: Contains the BSP (Binary Space Partitioning) class. This class is responsible for managing the game's level geometry, enabling efficient rendering and collision detection.
- `data_types.py`: Defines various data types, classes, and structures used throughout the project. This could include things like vector and matrix classes, enums, etc.
- `map_renderer.py`: Contains the MapRenderer class which is responsible for drawing the game world based on the current player position and the level data.
- `player.py`: Contains the Player class which handles player character behavior, such as movement, shooting, and health tracking.
- `seg_handler.py`: Contains the SegHandler class which handles segments, which are parts of linedefs, a crucial element of the level data in DOOM.
- `settings.py`: Contains global game settings and constants, like screen resolution, controls, and game rules.
- `view_renderer.py`: Contains the ViewRenderer class which is responsible for rendering the player's first-person perspective view of the world.
- `wad_data.py`: Contains the WadData class which is responsible for loading and parsing the data from the WAD file(s).
- `wad_reader.py`: Contains the WadReader class which is responsible for reading the raw data from the WAD file(s) and passing it to WadData for further processing.

### `resources`

This folder contains various resources used in the game:

#### `wad`

This subfolder contains the `DOOM1.WAD` file, which includes the data (levels, textures, sounds, etc.) for the original DOOM game.

## Instructions

To run the project, follow these steps:

1. Install Python 3 if you haven't already.
2. Install the Pygame library by running the command: `pip install pygame`.
3. Navigate to the project's `src` directory.
4. Run the command: `python3 src/main.py`.

Make sure you have the required resources in the appropriate directories as shown in the folder structure.

Feel free to modify and explore the engine to suit your needs.

Enjoy playing!

---
