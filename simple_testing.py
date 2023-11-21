import kesslergame
from kesslergame.scenario import Scenario
from controllers.basic_controller import BasicController
from controllers.fuzzy_tree_controller import FuzzyController

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=1)
controllers = [FuzzyController()]

game.run(scenario, controllers)

