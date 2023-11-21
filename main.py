import kesslergame
from kesslergame.scenario import Scenario
from my_controller import TestController

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=20)
controllers = [TestController()]

game.run(scenario, controllers)

