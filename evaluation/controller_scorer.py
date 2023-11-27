import kesslergame
from kesslergame.kessler_game import TrainerEnvironment, KesslerGame
from kesslergame.scenario import Scenario
from kesslergame.controller import KesslerController
from controllers.genetic_fuzzy import genetic_controller
import numpy as np

# game = TrainerEnvironment()  # Use this instead if you want NO GUI
game = KesslerGame()
scenario = Scenario(name='test', num_asteroids=15)

def evaluate_controller(controller: KesslerController) -> float:
    results = []
    num = 1
    for _ in range(num):
        info = game.run(scenario, [controller])

        # My god this is a hard number to get
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

# def main():
#     from controllers. import SimpleFuzzy
#     score = evaluate_controller(SimpleFuzzy())
#     print(score)

# if __name__ == '__main__':
#     main()