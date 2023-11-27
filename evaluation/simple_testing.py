import kesslergame
from kesslergame.scenario import Scenario
from controllers.basic_controller import BasicController
from controllers.fuzzy_tree_controller import FuzzyController
from controllers.genetic_fuzzy import GeneticFuzzy
from controllers.fuzzy_discrete_danger import DangerFuzzy

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=1)

values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
print(values)
controllers = [GeneticFuzzy(values)]

game.run(scenario, controllers)

