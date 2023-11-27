import kesslergame
import time
from kesslergame.kessler_game import TrainerEnvironment, KesslerGame
from kesslergame.scenario import Scenario
from kesslergame.controller import KesslerController
from controllers.genetic_fuzzy import genetic_controller
import numpy as np

# game = TrainerEnvironment()  # Use this instead if you want NO GUI
game = KesslerGame()
scenario = Scenario(name='test', num_asteroids=10)

def evaluate_controller(controller: KesslerController) -> float:
    # results = []
    times = []
    num = 1
    
    start = time.time()

    for _ in range(num):
        info = game.run(scenario, [controller])

        # My god this is a hard number to get
        score_obj = info[0]
        team = score_obj.teams[0]
        score = team.asteroids_hit
        # results.append(score)
        time_elapsed = time.time() - start
        lives_remaining = team.lives_remaining
        if lives_remaining == 0:
            print('Did not clear screen. Setting time as 1000000')
            time_elapsed = 1000000
        times.append(time_elapsed)
    # results.sort()
    times.sort()
    # true_score = np.average(results[0:num])
    average_time = np.average(times[0:num])    

    # return true_score
    return average_time

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