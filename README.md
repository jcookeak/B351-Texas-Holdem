# B351-Texas-Holdem
Texas Hold'em Final Project

## Current Status
1. Running through the game multiple times results in the same winner each time, even with
2. can run multiple games with command: seq 50 | xargs -Iz python3 game.py
3. todo implement betting strategy
4. todo: implement better calling for different hand classes
5. Chips appear to be broken again.
6. Raising is causing problems
7. Occasional division by zero error


Added a new file to fix the chip situation: game_mechanics.py
Went through the game file line by line and transformed it into this file
It occasionally adds one chip into the game, however, most of the time it seems to work.
Still looking into why one chip pops up every so often.
