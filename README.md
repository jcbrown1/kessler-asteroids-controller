# DESIGN DOCUMENT
https://docs.google.com/document/d/1dESp02CtQHdKuoQ7bPWhjdPxBb_Zvr5CH5_EGJl696M/edit?usp=sharing

# kessler-asteroids-controller
Genetic algorithm optimized fuzzy tree to play the kessler-game implemented by Thales Group

# How to Setup:
It is recommended to use a virtual environment to ensure no conflicting dependencies. However, there are no
unexpected libraries and the grader of this may not even need to manually add any at all. 
```
pip install -r requirements.txt
```
# File Explanation:
`evaluation/genetic_training.py` -> This is the main file to run to train a genetic fuzzy system
`evaluation/controller_scorer.py` -> This is a module containing the fitness function for genetic training. It does not need to be run in isolation
`evaluation/controllers/genetic_fuzzy.py` -> This is the genetic fuzzy controller that implements genetically trained parameters. To use it as a normal controller, use the `genetic_controller()` function with NO ARGUMENT in kessler game.
`evaluation/controllers/simple_fuzzy.py` -> This is a basic fuzzy ccontroller. It is used as the base class of the genetic fuzzy controller and isn't meant to be run in isolation, but it can be if desired.
