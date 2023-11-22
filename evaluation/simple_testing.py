import kesslergame
from kesslergame.scenario import Scenario
from controllers.basic_controller import BasicController
from controllers.fuzzy_tree_controller import FuzzyController
from controllers.fuzzy_discrete_danger import DangerFuzzy

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=20)
controllers = [DangerFuzzy()]

game.run(scenario, controllers)

