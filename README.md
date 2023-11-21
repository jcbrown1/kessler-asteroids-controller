# kessler-asteroids-controller
Genetic algorithm optimized fuzzy tree to play the kessler-game implemented by Thales Group

# How to Setup:
Go to the releases page
https://github.com/ThalesGroup/kessler-game/releases

install V1.3.6

pip install the extracted folder

You will also need some basic scientific computing libraries (numpy, scikit-fuzzy, etc) but the list is going to change often

# TODO

1. Implement a fuzzy-tree
   - Determine rules
   - What info are we going to input into the tree?
        - ship distance from center
        - closest asteroid RELATIVE position
             - polar coordinates
        - closest asteroid velocity
             - polar coordinates
        - bullet velocity?
        - closest asteroid in front relative position
             - distance (no angle)
        - closest asteroid behind relative position
             - distance (no angle)
        - closest asteroid to the left relative position
             - distance (no angle)
        - closest asteroid to the right relative positon
             - distance (no angle)
      
2. Create testing function to evaluate performance of a controller
   - five runs, average the score (number of killed asteroids)
3. Re-do parts of fuzzy tree to be genetic so we can train this bitch 
