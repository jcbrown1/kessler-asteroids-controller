from typing import Dict, Tuple

import numpy as np

import skfuzzy as fuzz
from skfuzzy import control as ctrl

from kesslergame import KesslerController
from kesslergame.asteroid import Asteroid


def create_fuzzy_system() -> ctrl.ControlSystemSimulation:

    # Antecedents
    target_angle_error = ctrl.Antecedent(np.linspace(-1, 1, 100), 'target_angle_error')
    target_asteroid_distance = ctrl.Antecedent(np.linspace(0, 1, 100), 'target_asteroid_distance')
    current_speed = ctrl.Antecedent(np.linspace(-1, 1, 100), 'current_speed')

    # Consequents
    linear_thrust = ctrl.Consequent(np.linspace(-1, 1, 100), 'linear_thrust')
    angular_thrust = ctrl.Consequent(np.linspace(-1, 1, 100), 'angular_thrust')
    fire_command = ctrl.Consequent(np.linspace(0, 1, 100), 'fire_command')

    # Membership Functions
    target_angle_error['very_left'] = fuzz.trimf(target_angle_error.universe, (-1, -1, -0.5))
    target_angle_error['little_left'] = fuzz.trimf(target_angle_error.universe, (-1, -0.5, 0))
    target_angle_error['center'] = fuzz.trimf(target_angle_error.universe, (-0.5, 0, 0.5))
    target_angle_error['little_right'] = fuzz.trimf(target_angle_error.universe, (0, 0.5, 1))
    target_angle_error['very_right'] = fuzz.trimf(target_angle_error.universe, (0.5, 1, 1))

    target_asteroid_distance['very_far'] = fuzz.trimf(target_asteroid_distance.universe, (0.75, 1, 1))
    target_asteroid_distance['far'] = fuzz.trimf(target_asteroid_distance.universe, (0.5, 0.75, 1))
    target_asteroid_distance['in_range'] = fuzz.trimf(target_asteroid_distance.universe, (0.25, 0.5, 0.75))
    target_asteroid_distance['close'] = fuzz.trimf(target_asteroid_distance.universe, (0, 0.25, 0.5))
    target_asteroid_distance['very_close'] = fuzz.trimf(target_asteroid_distance.universe, (0, 0, 0.25))

    current_speed['fast_reverse'] = fuzz.zmf(current_speed.universe, -1, -0.5)
    current_speed['slow_reverse'] = fuzz.trimf(current_speed.universe, (-1, -0.5, 0))
    current_speed['stop'] = fuzz.trimf(current_speed.universe, (-0.5, 0, 0.5))
    current_speed['slow_forward'] = fuzz.trimf(current_speed.universe, (0, 0.5, 1))
    current_speed['fast_forward'] = fuzz.smf(current_speed.universe, 0.5, 1)

    linear_thrust['fast_reverse'] = fuzz.trimf(linear_thrust.universe, (-1, -1, -0.5))
    linear_thrust['slow_reverse'] = fuzz.trimf(linear_thrust.universe, (-1, -0.5, 0))
    linear_thrust['stop'] = fuzz.trimf(linear_thrust.universe, (-0.5, 0, 0.5))
    linear_thrust['slow_forward'] = fuzz.trimf(linear_thrust.universe, (0, 0.5, 1))
    linear_thrust['fast_forward'] = fuzz.trimf(linear_thrust.universe, (0.5, 1, 1))

    angular_thrust['fast_left'] = fuzz.trimf(angular_thrust.universe, (-1, -1, -0.5))
    angular_thrust['slow_left'] = fuzz.trimf(angular_thrust.universe, (-1, -0.5, 0))
    angular_thrust['stop'] = fuzz.trimf(angular_thrust.universe, (-0.5, 0, 0.5))
    angular_thrust['slow_right'] = fuzz.trimf(angular_thrust.universe, (0, 0.5, 1))
    angular_thrust['fast_right'] = fuzz.trimf(angular_thrust.universe, (0.5, 1, 1))

    fire_command['no'] = fuzz.zmf(fire_command.universe, 0.4, 0.6)
    fire_command['yes'] = fuzz.smf(fire_command.universe, 0.4, 0.6)
    
    # Rules
    rules = []

    rules.append(ctrl.Rule(target_asteroid_distance['very_far'] & current_speed['fast_forward'], linear_thrust['slow_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['very_far'] & current_speed['slow_forward'], linear_thrust['stop']))
    rules.append(ctrl.Rule(target_asteroid_distance['very_far'] & current_speed['stop'], linear_thrust['slow_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['very_far'] & (current_speed['slow_reverse'] | current_speed['fast_reverse']), linear_thrust['fast_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['far'] & current_speed['fast_forward'], linear_thrust['fast_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['far'] & current_speed['slow_forward'], linear_thrust['stop']))
    rules.append(ctrl.Rule(target_asteroid_distance['far'] & current_speed['stop'], linear_thrust['slow_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['far'] & (current_speed['slow_reverse'] | current_speed['fast_reverse']), linear_thrust['fast_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['in_range'] & current_speed['fast_forward'], linear_thrust['fast_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['in_range'] & current_speed['slow_forward'], linear_thrust['slow_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['in_range'] & current_speed['stop'], linear_thrust['stop']))
    rules.append(ctrl.Rule(target_asteroid_distance['in_range'] & current_speed['slow_reverse'], linear_thrust['slow_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['in_range'] & current_speed['fast_reverse'], linear_thrust['fast_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['close'] & (current_speed['slow_forward'] | current_speed['fast_forward']), linear_thrust['fast_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['close'] & current_speed['stop'], linear_thrust['slow_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['close'] & current_speed['slow_reverse'], linear_thrust['stop']))
    rules.append(ctrl.Rule(target_asteroid_distance['close'] & current_speed['fast_reverse'], linear_thrust['slow_forward']))
    rules.append(ctrl.Rule(target_asteroid_distance['very_close'] & (current_speed['stop'] | current_speed['slow_forward'] | current_speed['fast_forward']), linear_thrust['fast_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['very_close'] & current_speed['slow_reverse'], linear_thrust['slow_reverse']))
    rules.append(ctrl.Rule(target_asteroid_distance['very_close'] & current_speed['fast_reverse'], linear_thrust['stop']))
    rules.append(ctrl.Rule(target_angle_error['very_left'] & current_speed['fast_forward'], (angular_thrust['fast_left'], linear_thrust['fast_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['very_left'] & current_speed['slow_forward'], (angular_thrust['fast_left'], linear_thrust['slow_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['very_left'] & current_speed['stop'], (angular_thrust['fast_left'], linear_thrust['stop'])))
    rules.append(ctrl.Rule(target_angle_error['very_left'] & current_speed['slow_reverse'], (angular_thrust['fast_left'], linear_thrust['slow_forward'])))
    rules.append(ctrl.Rule(target_angle_error['very_left'] & current_speed['fast_reverse'], (angular_thrust['fast_left'], linear_thrust['fast_forward'])))
    rules.append(ctrl.Rule(target_angle_error['little_left'] & current_speed['fast_forward'], (angular_thrust['slow_left'], linear_thrust['fast_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['little_left'] & current_speed['slow_forward'], (angular_thrust['slow_left'], linear_thrust['slow_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['little_left'] & current_speed['stop'], (angular_thrust['slow_left'], linear_thrust['stop'])))
    rules.append(ctrl.Rule(target_angle_error['little_left'] & current_speed['slow_reverse'], (angular_thrust['slow_left'], linear_thrust['slow_forward'])))
    rules.append(ctrl.Rule(target_angle_error['little_left'] & current_speed['fast_reverse'], (angular_thrust['slow_left'], linear_thrust['fast_forward'])))
    rules.append(ctrl.Rule(target_angle_error['center'], angular_thrust['stop']))
    rules.append(ctrl.Rule(target_angle_error['little_right'] & current_speed['fast_forward'], (angular_thrust['slow_right'], linear_thrust['fast_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['little_right'] & current_speed['slow_forward'], (angular_thrust['slow_right'], linear_thrust['slow_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['little_right'] & current_speed['stop'], (angular_thrust['slow_right'], linear_thrust['stop'])))
    rules.append(ctrl.Rule(target_angle_error['little_right'] & current_speed['slow_reverse'], (angular_thrust['slow_right'], linear_thrust['slow_forward'])))
    rules.append(ctrl.Rule(target_angle_error['little_right'] & current_speed['fast_reverse'], (angular_thrust['slow_right'], linear_thrust['fast_forward'])))
    rules.append(ctrl.Rule(target_angle_error['very_right'] & current_speed['fast_forward'], (angular_thrust['fast_right'], linear_thrust['fast_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['very_right'] & current_speed['slow_forward'], (angular_thrust['fast_right'], linear_thrust['slow_reverse'])))
    rules.append(ctrl.Rule(target_angle_error['very_right'] & current_speed['stop'], (angular_thrust['fast_right'], linear_thrust['stop'])))
    rules.append(ctrl.Rule(target_angle_error['very_right'] & current_speed['slow_reverse'], (angular_thrust['fast_right'], linear_thrust['slow_forward'])))
    rules.append(ctrl.Rule(target_angle_error['very_right'] & current_speed['fast_reverse'], (angular_thrust['fast_right'], linear_thrust['fast_forward'])))

    fuzzy_ctrl = ctrl.ControlSystem(rules)
    fuzzy_sim = ctrl.ControlSystemSimulation(fuzzy_ctrl)

    return fuzzy_sim


class HughMungus(KesslerController):
    def __init__(self):
        """
        Any variables or initialization desired for the controller can be set up here
        """
        values = [0.80857, 0.76046, 0.922634, 0.755019]

        sim = create_fuzzy_system()
        self.sim = sim

        self.target_distance = remap(get(values, 1), 150, 250)
        self.angle_max = 180
        self.max_speed = remap(get(values, 1), 350, 500)

        self.linear_scaling = remap(get(values, 1), 400, 550)
        self.angular_scaling = remap(get(values, 1), 450, 550)
        self.eval_frames = 0  # required field in scenario test


    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool, bool]:
        """
        Method processed each time step by this controller to determine what control actions to take

        Arguments:
            ship_state (dict): contains state information for your own ship
            game_state (dict): contains state information for all objects in the game

        Returns:
            float: thrust control value
            float: turn-rate control value
            bool: fire control value. Shoots if true
        """
        self.ship_state = ship_state
        self.game_state = game_state

        self.update_derived_features()

        command = self.get_command()

        self.eval_frames +=1

        return command

    def get_command(self) -> tuple[float]:
        sim = self.sim

        target_distance = self.target_distance
        angle_max = self.angle_max
        max_speed = self.max_speed

        linear_scaling = self.linear_scaling
        angular_scaling = self.angular_scaling

        sim.input['target_angle_error'] = normalize(self.target_angle_error, angle_max, symmetric=True)
        sim.input['target_asteroid_distance'] = normalize(self.target_asteroid_distance, target_distance)
        sim.input['current_speed'] = normalize(self.ship_speed, max_speed, symmetric=True)

        sim.compute()

        linear_thrust = sim.output['linear_thrust'] * linear_scaling
        linear_thrust = self.clip_linear_thrust(linear_thrust)

        angular_thrust = sim.output['angular_thrust'] * angular_scaling
        angular_thrust = self.clip_angular_thrust(angular_thrust)

        fire_command = True

        command = (linear_thrust, angular_thrust, fire_command)

        return command
    
    def get_closest_asteroid(self, ship_state: Dict, game_state: Dict) -> Asteroid.state:
        closest_distance = 1000000
        closest_state = None

        my_position = self.ship_state['position']
        my_position = np.array(my_position)

        for asteroid_state in self.game_state['asteroids']:
            their_position = np.array(asteroid_state['position'])
            vector_diff = np.array(my_position - their_position)
            distance_diff = np.linalg.norm(vector_diff) - asteroid_state['size']
            
            if closest_distance > distance_diff:
                closest_distance = distance_diff
                closest_state = asteroid_state

        return closest_state

    def get_asteroid_distance_angles(self, ship_state: Dict, game_state: Dict) -> list[tuple]:
        '''
        returns list of asteroids as pair of numbers
        (distance from ship, angle from positive x-axis in degrees)
        '''

        map_size = self.game_state['map_size']

        ship_heading = self.ship_state['heading']
        ship_angle = 90 - ship_heading

        pairs = []

        for asteroid_state in self.game_state['asteroids']:
            d_vec = np.array(self.ship_state['position']) - np.array(asteroid_state['position'])
            if d_vec[0] > map_size[0]/2:
                d_vec[0] = map_size[0] - d_vec[0]
            if d_vec[1] > map_size[1]/2:
                d_vec[1] = map_size[1] - d_vec[1]

            d_norm = np.linalg.norm(d_vec)
            d_angle = np.arctan2(d_vec[1], d_vec[0])
            d_angle = np.rad2deg(d_angle)
            d_angle = ((d_angle - ship_angle) % 360) - 180

            pairs.append((d_norm, d_angle))

        return pairs
            

    def update_derived_features(self) -> None:
 
        self.update_target_angle_error()
        self.update_ship_velocity()

    def update_target_angle_error(self) -> None:
        closest_asteroid = self.get_closest_asteroid(self.ship_state, self.game_state)
        
        if closest_asteroid is None:
            print('No closest asteroid?')
            return 0.0

        my_angle = self.ship_state['heading']

        vec_pos_diff = np.array(closest_asteroid['position']) - np.array(self.ship_state['position'])
        vel_asteroid = closest_asteroid['velocity']
        bullet_speed = 800

        a = bullet_speed**2 - np.linalg.norm(vel_asteroid)**2
        b = -2 * np.dot(vec_pos_diff, vel_asteroid)
        c = - np.linalg.norm(vec_pos_diff)**2                                               
        b2 = b / a
        c2  = c / a 

        t1 = (-b2 + np.sqrt(b2**2 - 4*c2))
        # t2 = (-b2 - np.sqrt(b2**2 - 4*c2))

        # t = max(t1, t2)
        t = t1

        y = vec_pos_diff[1] + vel_asteroid[1] * t
        x = vec_pos_diff[0] + vel_asteroid[0] * t
        set_point_angle = np.rad2deg(np.arctan2(y, x))

        # DETERMINE THETA

        error = (my_angle - set_point_angle) % 360
        if error > 180:
            error -= 360

        self.target_angle_error = -error
        self.target_asteroid_distance = np.linalg.norm(vec_pos_diff)

    def update_ship_velocity(self) -> None:
        speed = self.ship_state['speed']
        self.ship_speed = speed

    def clip_linear_thrust(self, linear_thrust) -> float:
        mn, mx = self.ship_state['thrust_range']
        bounded_thrust = np.clip(linear_thrust, mn, mx)
        return bounded_thrust
    
    def clip_angular_thrust(self, angular_thrust) -> float:
        mn, mx = self.ship_state['turn_rate_range']
        bounded_thrust = np.clip(angular_thrust, mn, mx)
        return bounded_thrust

    @property
    def name(self) -> str:
        """
        Simple property used for naming controllers such that it can be displayed in the graphics engine

        Returns:
            str: name of this controller
        """
        return "Hugh Mungus"


def normalize(num, mx, symmetric=False):
    if symmetric:
        mn = -mx
    else:
        mn = 0
    
    normal = np.clip(num, mn, mx) / mx
    return normal

def remap(num, mn, mx):
    diff = mx - mn
    return num * diff + mn

def get(values: list[float], num: int) -> list[float]:
    sublist = []
    for _ in range(num):
        sublist.append(values.pop())
    sublist.sort()
    
    if num == 1:
        return sublist[0]
    return sublist