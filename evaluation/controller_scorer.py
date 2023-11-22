import kesslergame
from kesslergame.scenario import Scenario
from kesslergame.controller import KesslerController
from controllers.fuzzy_tree_controller import FuzzyController
from controllers.fuzzy_discrete_danger import DangerFuzzy

import numpy as np

game = kesslergame.kessler_game.KesslerGame()
scenario = Scenario(name='test', num_asteroids=20)

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

def main():
    score = evaluate_controller(DangerFuzzy())
    print(score)
    

if __name__ == '__main__':
    main()