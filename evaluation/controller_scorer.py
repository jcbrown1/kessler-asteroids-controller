from kesslergame import GraphicsType
import time
from kesslergame.kessler_game import TrainerEnvironment, KesslerGame
from kesslergame.scenario import Scenario
from kesslergame.controller import KesslerController
from controllers.genetic_fuzzy import genetic_controller
from controllers.winner_winner_chicken_dinner import HughMungus
import numpy as np

# game = TrainerEnvironment()  # Use this instead if you want NO GUI
game_settings = {'perf_tracker': True,
 'graphics_type': GraphicsType.Tkinter,
 'realtime_multiplier': 1,
 'graphics_obj': None}

game = KesslerGame(game_settings)
scenario = Scenario(
    name='test', 
    num_asteroids=10,
    # asteroid_states=[
    #                 {'position' : (100, 100),'angle': 45, 'speed' : np.random.randint(10, 50), 'size' : np.random.randint(3, 4)},
    #                 {'position' : (900, 100), 'angle' : 135, 'speed' : np.random.randint(10, 50)},
    #                 {'position' : (900, 700), 'angle' : 225, 'speed' : np.random.randint(10, 50), 'size' : np.random.randint(3, 4)},
    #                 {'position' : (100, 700), 'angle' : 315, 'speed' : np.random.randint(10, 50)},
    #                 {'position' : (500, 100), 'angle' : 90, 'speed' : np.random.randint(10, 50)},
    #                 {'position' : (100, 400), 'angle' : 0, 'speed' : np.random.randint(10, 50)},
    #                 {'position' : (900, 400), 'angle' : 180, 'speed' : np.random.randint(10, 50)},
    #                 {'position' : (500, 700), 'angle' : 270, 'speed' : np.random.randint(10, 50)}
    #             ],
    )

def evaluate_controller(controller: KesslerController) -> float:
    results = []
    # times = []
    num = 10
    
    start = time.time()

    for _ in range(num):
        info = game.run(scenario, [controller])

        # My god this is a hard number to get
        score_obj = info[0]
        team = score_obj.teams[0]
        score = team.asteroids_hit
        print(f'Score {num} is {score}')
        results.append(score)
        time_elapsed = time.time() - start
        lives_remaining = team.lives_remaining
        # if lives_remaining == 0:
        #     print('Did not clear screen. Setting time as 1000000')
        #     time_elapsed = 1000000
        # times.append(time_elapsed)
    results.sort()
    # times.sort()
    true_score = np.average(results[0:num])
    # average_time = np.average(times[0:num])    
    print(f'Average {true_score}')

    return true_score
    # return average_time

def evaluate_chromosome(chromosome):
    controller = genetic_controller(chromosome)
    score = evaluate_controller(controller)
    return score

def main():
    score = evaluate_controller(HughMungus())
    print(score)

if __name__ == '__main__':
    main()