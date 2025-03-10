# TODO
- [x] Add logging for object instantiation (game pieces, players, etc.)
- [x] Add logging for game state changes
- [x] Add logging for important game events
- [x] Add logging for errors and warnings
- [x] Add logging for player actions
    Added: 
        Creates a singleton logger class
        Sets up both file and console logging
        Creates a logs directory if it doesn't exist
        Uses different log levels for different types of events
        Integrates logging into core game components
        Timestamps all log entries
        Provides both debug (file) and info (console) outputs

## Games
- [x] Implement a second game in engine
    Added:
        Puzzle Fighter
- [x] Add controls attribute to Game base class for setting controls for each game
- [x] !! Change Tetris to use more of the TMGE engine.  (Grid functions -> TetrisGrid, Tile functions, etc.)

## Engine
- [x] Player count + 2p options in `Game ABC`
- [x] Game start/restart/exit options in `Game ABC` use case example: user gets game over in tetris, user can either restart the game or exit to main menu. This popup is up to the developer to implement.
- [x] in `GameABC`, check win condition and check loss condition.
- [x] in `Grid`, check tile matches, clearing, and valid movement
- [x] in `Tile`, add `tile_shape`, `tile_color`, `tile_state`, `position` (x,y : top left corner of tile)
    Added: 
        All of the above

## Design
- [x] Port & Update UML

# ISSUES

- [x] !! Logout button exits entire program but should just return to main menu.
- [x] I think making new profiles overides old ones in profiles.json.
    + Not an issue for me when I ran it, need to replicate it on Sierra's computer

## CHANGES
- [x] Add controls to game_controls_dict in main.py
- [x] Add controls to home window in home_window.py -> passed from tmge_application
- [x] add space to puzzle fighter controls dict key


## JOSH FEEDBACK
- [x] Remember to return an unmodifiable getters. Otherwise, profiles may leak to other classes that may modify by accident. 
    - `@property` - allows methods to be accessed like attributes (makes it read-only)

- [x] There probably should be a gameLoop() method of some kind. What kind of design pattern(s) are good for this interface? 
    - IInputHandler and IGameLoop implement an update/draw/init that functions as our game loop

- [x] At this point, it's probably better to explicitly include the library elements your TMGE or games will build on top of or extend and use them and their constituents methods in your design (e.g., the Application, Stage, and Scene classes in JavaFX). (● draw(): Renders the game to the screen. Called repeatedly in the game loop.)

- [x] You can replace these event handlers/callback methods with whatever UI/GUI framework you end up deciding to use. (● handleKeyPress(KeyEvent): Processes key press events. ● handleKeyRelease(KeyEvent): Processes key release events)

- [x] Hmm. Would this be best operating in your currently missing gameLoop() method in your IGameLoop? (checkWinCondition())
    - Updated / Moved to Game class
    - IInputHandler and IGameLoop implement an update/draw/init that functions as our game loop

- [x] The matching criteria or algorithms are first-class entities in a tile-matching games. They should probably be classifiers (e.g., UML interfaces or classes). In fact, what design pattern would be a good fit for your Matching classifier?

- [ ] Identify as many opportunities for design patterns that would help improve your design and implementation and mark them up in your UML design (e.g., use a UML note).

- [ ] Will your games be turn-based or real-time? I don't see a Clock class or interface, so it looks like it will be turn-based. 
    - update is our clock ticker

**Template**
    - Not enough operations, need very fixed skeletal structure
    - [x] **professor said look at `Game` ABC. Claude says we must add `play() `method**
        ```py
            ' Template method that defines the game algorithm
        +final play(): void {
            initializeGame()
            while(!isGameOver()) {
            processInput()
            updateGameState()
            renderGame()
            if(checkWinCondition()) {
                    handleWinCondition()
                }
            }
            endGame()
        }
        ```
