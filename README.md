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
        - ship distance from center? (Probably a bad call)
        - ship heading? (maybe just use the error of your heading and the target distance...)
        - diff between heading and target relative angle
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
   - Consider remapping coordinates of dangerous asteroids to account for edge of screen position jump
   - angular_thrust output rules and membership shoould be symmetric,
with smallest output meaning left and largest meaning right

CONSIDER THE FOLLOWING TREE STRUCTURE:
```
                        if so, get away
determine if in danger
                        if not, shoot an easy asteroid

            in parallel, determine whether or not to shoot
```
            
2. Create testing function to evaluate performance of a controller
   - five runs, average the score (number of killed asteroids)
3. Re-do parts of fuzzy tree to be genetic so we can train this bitch 
