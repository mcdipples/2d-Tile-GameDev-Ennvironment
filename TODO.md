# TODO
- [ ] Add scoring system to player profile
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
- [ ] Add controls attribute to Game base class for setting controls for each game
- [ ] !! Change Tetris to use more of the TMGE engine.  (Grid functions -> TetrisGrid, Tile functions, etc.)

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
