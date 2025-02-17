# 2d-Tile-GameDev-Ennvironment

# Description 

Design and implement an extensible Tile-Matching Game Environment (TMGE).  We will adhere to the definition of a tile-matching game as used in this Wikipedia articleLinks to an external site..
Work in teams of 4-5 students
We will spend time in class to help everyone find a team in a timely manner. If you have excessive difficulty finding a team, we will assign you to one.
Requirements 

The TMGE should accommodate any tile-matching game that involves a grid layout and game elements on this layout, including games such as Tetris, Klax, Bejeweled, Bust-a-Move, Puzzle Bobble, Candy Crush, Dr. Mario, Puzzle Fighter, etc. 
The TMGE should make it as easy as possible to create implementations of new games.
The TMGE should provide a defined interface that all games built on top of the environment must follow.
The TMGE should support two players running on the same local machine.
The TMGE should support personal player profiles (the specifics of which are up to you). Login can be very simple and does not have to be secure.
The TMGE need only support 2-player games (but you can support more players if you want to).
The TMGE should work by providing players with a list of games they can play and allowing them to choose which one to start.
Deliverables

The TMGE itself
Two or more tile-matching games (e.g., from the list above) that are "built on top of" the TMGE. 
Documentation
Instructions for running the game
Runnable code via a CM repository like GitHub (e.g., add a runnable jar to your GitHub repo)
Peer evaluations (will be made available to you)
Reuse 

Cannot pick up an existing game environment implementation
You can reuse other components, but first, double-check with the professor
Grading Criteria 

Stakeholder: the player (how is the experience of playing a game?)
Stakeholder: future developers of the TMGE (how is the understandability and quality of the code and design?)
Stakeholder: game developers (how is the extensibility of the TMGE in supporting new board games? how well do you hide parts of TMGE that should not be exposed to game developers? how is the experience of building in a new game using your TMGE?)
Stakeholder: you (what are your contributions to the project?)
A GUI is not required but may actually make your project easier to implement.
Miscellaneous 

Mark clearly in your design/architecture the places that are variant (variable per game) and which are fixed
Use a configuration management repository (this is good practice, but we will also use it to verify who wrote which code -- check in your own code!). Give the professor and the TA/Reader access via email.
All group members do not have to present each time. You can split up the presentation work however you want.
Design, Implementation, and Team Meetups in Class:

We will have several weeks of in-class sessions where you can meet with the team, the professor, or the TA to discuss your design and implementation. Please come to class and make use of these sessions.
Last Two Weeks of the Quarter:

Final demo: Run your TMGE and implemented games in front of instructors (max 10 minutes per team)

Final (updated) design document and a retrospective on your design, including UML with description/explanation, and step-by-step instructions for how to make a new game using TMGE. Also, include a description of how and why this updated design evolved from your original design. Include high points, low points, and major challenges you experienced in this phase and in the project as a whole. Turn this document into THIS assignment on Canvas.
Peer evaluations will be made available to you
Suggestions

Split your team into sub-teams. Because teams are large, it will be most efficient if you divide your team up based on the parts of the problem. Also, consider appointing a team lead (or two?) to make things more efficient. Be sure one of these sub-teams is dedicated to architecture/interface management between the separate parts.
Use a group communication/coordination tool. e.g., Slack or something like it.
Think about what every game will have in common, then build abstractions for the commonality or variability (e.g., interfaces/abstract classes).
Extra Credit

Design and implement a GUI for your TMGE and its games (3% extra credit)
Have your TMGE and at least one game support real-time play (3% extra credit)
