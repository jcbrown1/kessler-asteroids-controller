import kesslergame
from kesslergame.scenario import Scenario
from controllers.basic_controller import BasicController
from controllers.fuzzy_tree_controller import FuzzyController
from controllers.simple_fuzzy import SimpleFuzzy
from controllers.fuzzy_discrete_danger import DangerFuzzy

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=15)
controllers = [SimpleFuzzy()]

game.run(scenario, controllers)

