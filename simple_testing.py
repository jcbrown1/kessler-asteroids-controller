import kesslergame
from kesslergame.scenario import Scenario
from controllers.basic_controller import BasicController

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=20)
controllers = [BasicController()]

game.run(scenario, controllers)

