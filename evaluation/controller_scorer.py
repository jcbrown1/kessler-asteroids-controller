import kesslergame
from kesslergame.kessler_game import TrainerEnvironment
from kesslergame.scenario import Scenario
from kesslergame.controller import KesslerController
from controllers.simple_fuzzy import genetic_controller
import numpy as np

game = TrainerEnvironment()
scenario = Scenario(name='test', num_asteroids=15)

def evaluate_controller(controller: KesslerController) -> float:
    results = []

    for _ in range(5):
        info = game.run(scenario, [controller])

        # My god this is a hard number to get
        score_obj = info[0]
        team = score_obj.teams[0]
        score = team.asteroids_hit
        results.append(score)

    results.sort()
    true_score = np.average(results[1:4])    

    return true_score

def evaluate_chromosome(chromosome):
    controller = genetic_controller(chromosome)
    score = evaluate_controller(controller)
    return score

def main():
    from controllers.simple_fuzzy import SimpleFuzzy
    score = evaluate_controller(SimpleFuzzy())
    print(score)

if __name__ == '__main__':
    main()