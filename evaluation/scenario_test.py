import time
from kesslergame import Scenario, KesslerGame, GraphicsType
from controllers.simple_fuzzy import SimpleFuzzy
from controllers.genetic_fuzzy import genetic_controller
from controllers.scott_dick_controller import ScottDickController
from graphics_both import GraphicsBoth

my_test_scenario = Scenario(name='Test Scenario',
 num_asteroids=5,
ship_states=[
 {'position': (400, 400), 'angle': 90, 'lives': 3, 'team': 1},
 {'position': (600, 400), 'angle': 90, 'lives': 3, 'team': 2},
 ],

map_size=(1000, 800),
 time_limit=60,
ammo_limit_multiplier=0,
stop_if_no_ammo=False)
game_settings = {'perf_tracker': True,
 'graphics_type': GraphicsType.Tkinter,
 'realtime_multiplier': 1,
 'graphics_obj': None}

def run_game():
    game = KesslerGame(settings=game_settings) # Use this to visualize the game scenario
    # game = TrainerEnvironment(settings=game_settings) # Use this for max-speed, no-graphics simulation
    pre = time.perf_counter()
    score, perf_data = game.run(scenario=my_test_scenario, controllers = [ScottDickController(), genetic_controller()])
    print('Scenario eval time: '+str(time.perf_counter()-pre))
    print(score.stop_reason)
    print('Asteroids hit: ' + str([team.asteroids_hit for team in score.teams]))
    print('Deaths: ' + str([team.deaths for team in score.teams]))
    print('Accuracy: ' + str([team.accuracy for team in score.teams]))
    print('Mean eval time: ' + str([team.mean_eval_time for team in score.teams]))
    print('Evaluated frames: ' + str([controller.eval_frames for controller in score.final_controllers]))

    return score.teams

def test_average_scores(num_games=5):
    team_sums = {"Team1":[0,0,0,0], "Team2":[0,0,0,0]}

    for _ in range(num_games):
        team_scores = run_game()
        for i, team in enumerate(team_scores):
            team_sums[f"Team{i + 1}"] = [s + v for s, v in zip(team_sums[f"Team{i + 1}"], [team.asteroids_hit, team.deaths, team.accuracy, team.mean_eval_time])]

    team_averages = {team: [s / num_games for s in sums] for team, sums in team_sums.items()}
    print("Metric : Scott vs GA Controller")
    for idx, metric in enumerate(["Asteroids Hit", "Deaths", "Accuracy", "Mean Eval Time"]):
        print(f"{metric}: {team_averages['Team1'][idx]} vs {team_averages['Team2'][idx]}")
    return team_averages

print(test_average_scores(5))






