# 2D Tile GameDev Ennvironment

## Prerequisites

- Python 3.9+
- pygame (for music)
- tkinter (for GUI)

## Installation

1. Clone/Download the repository
2. Install dependencies:

```
pip install pygame
pip install tkinter
```

## How to Run

Launch in root project's directory:
```
python main.py
- or -
python3 main.py
```

## Add Games

### Step One: Creating GamePiece Class

- All implemented concrete classes of ImplementedGame and GamePieces should be stored in the 'games' folder, as shown below

- Starting with the GamePiece classes, we want to store them in their `.py` file (e.g., `new_piece.py`). This is where we generally define the logic for how the pieces move, their positioning on the grid, and their visualization in the GUI for the ImplementedGame class (e.g., shape and color). In the example below, I will demonstrate a code snippet showing how to define the shapes, colors, constructor, move function, rotate function, and position getter function

### Step Two: Creating ImplementedGame Concrete Class

- All implemented concrete classes of ImplementedGame and GamePieces should be stored in the `games/` folder, as shown below

- Starting with the ImplementedGame concrete classes, we want to store them in their own `.py` file (e.g., `new_game.py`). It will then require the following imports, as shown below.

- After importing the classes from the games folder, we will create the ImplementedGame concrete class with the Game class as a parameter, which will implement all of its abstract methods. Additionally, it is important to provide values for `min_players` and `max_players`, as these are class-level attributes that store data shared among all instances of the class.

- Moving on to the constructor of the class, it takes the parameters self, `game_id`, and players, while also calling the parent class constructor and passing it `game_id`, rows, columns, and players. This is typically the function where you can create a grid (either multiple or single) based on specific criteria, as well as configure the controls. In the example below, I will create a 20x10 grid for a specified number of players (1-2) and set up the control configurations.

- Next, for the `initialize_game` abstract method, we can declare the variables needed for our game. In the example below, I provide an array of two GamePiece class objects that already have the logic implemented and are generated for the grid, as well as the scores for the two players and the starting status of each player's game.

- The same goes for the `check_win_condition` and `check_loss_condition` abstract method in terms of providing a declaration of what it is supposed to do for this specific game.

- These are just the basics or main requirements for implementation of a new game to be built off the TGME class defined by our team, but as you can see below of the complete remaining example code we are able to add more methods or add onto existing ones to meet the requirements of our game.

### Step Three: Update `main.py`

- After creating both the ImplementedGame concrete class and the GamePiece class within the `games/` folder, we can move on to adding this new game to the TGME system. This can all be done in the `main.py` file in the root folder of the project. First, we just need to import the ImplementedGame concrete class from the ‘games’ folder, as shown below.

- Lastly, within the `show_main_window` method of the TMGEApplication class, all we need to do is assign a variable to the constructor of the ImplementedGame concrete class, passing the appropriate parameter to create an object of that class. This object will then be passed into the tmge.`register_game` method to be added to the main window’s game selection screen, allowing users to choose it from their list of available games.

- You should see the game listed after running `main.py`, logging in, and accessing the game selection screen in the main menu.

## Add Music

1. Add your mp3 to the `music` directory
2. In your game's source code, set `self.music_path` to the file path of your mp3 in `music`

- Note: Games only support one song, and will loop until the window is closed
