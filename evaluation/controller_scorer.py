from kesslergame import GraphicsType
from kesslergame.kessler_game import KesslerGame
from kesslergame.scenario import Scenario
from kesslergame.controller import KesslerController
from controllers.genetic_fuzzy import genetic_controller
import numpy as np

game_settings = {'perf_tracker': True,
 'graphics_type': GraphicsType.Tkinter,
 'realtime_multiplier': 1,
 'graphics_obj': None}

game = KesslerGame(game_settings)
scenario = Scenario(
    name='test', 
    num_asteroids=10,)

def evaluate_controller(controller: KesslerController) -> float:
    results = []
    num = 5
    
    for _ in range(num):
        info = game.run(scenario, [controller])

        score_obj = info[0]
        team = score_obj.teams[0]
        score = team.asteroids_hit
        results.append(score)

    results.sort()
    true_score = np.average(results[0:num]) 

    return true_score

def evaluate_chromosome(chromosome):
    controller = genetic_controller(chromosome)
    score = evaluate_controller(controller)
    return score

def main():
    score = evaluate_controller(genetic_controller())
    print(score)

if __name__ == '__main__':
    main()