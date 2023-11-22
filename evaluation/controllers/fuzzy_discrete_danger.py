from typing import Dict, Tuple

import numpy as np

import skfuzzy as fuzz
from skfuzzy import control as ctrl

from kesslergame import KesslerController
from kesslergame.asteroid import Asteroid
from kesslergame.ship import Ship


class Sims():
    def __init__(
            self,
            danger_sim,
            fire_sim,
            attack_linear_sim,
            attack_angular_sim,
            escape_linear_sim,
            escape_angular_sim
            ):
        
        self.danger_sim = danger_sim
        self.fire_sim = fire_sim
        self.attack_linear_sim = attack_linear_sim
        self.attack_angular_sim = attack_angular_sim
        self.escape_linear_sim = escape_linear_sim
        self.escape_angular_sim = escape_angular_sim


def create_fuzzy_system() -> Sims:

    # Antecedents
    target_angle_error = ctrl.Antecedent(np.linspace(-1, 1, 100), 'target_angle_error')
    closest_danger_front = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_front')
    closest_danger_back = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_back')
    closest_danger_left = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_left')
    closest_danger_right = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_right')
    distance_net_front = ctrl.Antecedent(np.linspace(-1, 1, 100), 'distance_net_front')
    distance_net_right = ctrl.Antecedent(np.linspace(-1, 1, 100), 'distance_net_right')
    ship_speed = ctrl.Antecedent(np.linspace(-1, 1, 100), 'ship_speed')

    # Consequents
    danger = ctrl.Consequent(np.linspace(0, 1, 100), 'danger')
    linear_thrust = ctrl.Consequent(np.linspace(-1, 1, 100), 'linear_thrust')
    angular_thrust = ctrl.Consequent(np.linspace(-1, 1, 100), 'angular_thrust')
    fire_command = ctrl.Consequent(np.linspace(0, 1, 100), 'fire_command')

    # Membership Functions
    target_angle_error['left'] = fuzz.trimf(target_angle_error.universe, (-1, -1, 0))
    target_angle_error['center'] = fuzz.trimf(target_angle_error.universe, (-1, 0, 1))
    target_angle_error['right'] = fuzz.trimf(target_angle_error.universe, (0, 1, 1))

    closest_danger_front['close'] = fuzz.trimf(closest_danger_front.universe, (0, 0, 1))
    closest_danger_front['far'] = fuzz.trimf(closest_danger_front.universe, (0, 1, 1))

    closest_danger_back['close'] = fuzz.trimf(closest_danger_back.universe, (0, 0, 1))
    closest_danger_back['far'] = fuzz.trimf(closest_danger_back.universe, (0, 1, 1))

    closest_danger_left['close'] = fuzz.trimf(closest_danger_left.universe, (0, 0, 1))
    closest_danger_left['far'] = fuzz.trimf(closest_danger_left.universe, (0, 1, 1))

    closest_danger_right['close'] = fuzz.trimf(closest_danger_right.universe, (0, 0, 1))
    closest_danger_right['far'] = fuzz.trimf(closest_danger_right.universe, (0, 1, 1))

    distance_net_front['front_distance'] = fuzz.trimf(distance_net_front.universe, (0, 1, 1))
    distance_net_front['equal'] = fuzz.trimf(distance_net_front.universe, (-1, 0, 1))
    distance_net_front['back_distance'] = fuzz.trimf(distance_net_front.universe, (-1, -1, 0))

    distance_net_right['right_distance'] = fuzz.trimf(distance_net_right.universe, (0, 1, 1))
    distance_net_right['equal'] = fuzz.trimf(distance_net_right.universe, (-1, 0, 1))
    distance_net_right['left_distance'] = fuzz.trimf(distance_net_right.universe, (-1, -1, 0))

    ship_speed['fast_forward'] = fuzz.trimf(ship_speed.universe, (0.5, 1, 1))
    ship_speed['slow_forward'] = fuzz.trimf(ship_speed.universe, (0, 0.5, 1))
    ship_speed['still'] = fuzz.trimf(ship_speed.universe, (-0.5, 0, 0.5))
    ship_speed['slow_backward'] = fuzz.trimf(ship_speed.universe, (-1, -0.5, 0))
    ship_speed['fast_backward'] = fuzz.trimf(ship_speed.universe, (-1, -1, -0.5))

    danger['no'] = fuzz.zmf(danger.universe, 0.4, 0.6)
    danger['yes'] = fuzz.smf(danger.universe, 0.4, 0.6)

    linear_thrust['reverse'] = fuzz.trimf(linear_thrust.universe, (-1, -1, 0))
    linear_thrust['stop'] = fuzz.trimf(linear_thrust.universe, (-1, 0, 1))
    linear_thrust['forward'] = fuzz.trimf(linear_thrust.universe, (0, 1, 1))

    angular_thrust['left'] = fuzz.trimf(angular_thrust.universe, (-1, -1, 0))
    angular_thrust['stop'] = fuzz.trimf(angular_thrust.universe, (-1, 0, 1))
    angular_thrust['right'] = fuzz.trimf(angular_thrust.universe, (0, 1, 1))

    fire_command['no'] = fuzz.zmf(fire_command.universe, 0.4, 0.6)
    fire_command['yes'] = fuzz.smf(fire_command.universe, 0.4, 0.6)

    # Escape Rules
    escape_linear1 = ctrl.Rule(distance_net_front['front_distance'] & ship_speed['fast_forward'], linear_thrust['stop'])
    escape_linear2 = ctrl.Rule(distance_net_front['front_distance'] & ship_speed['slow_forward'], linear_thrust['forward'])
    escape_linear3 = ctrl.Rule(distance_net_front['front_distance'] & (ship_speed['still'] | ship_speed['slow_backward'] | ship_speed['fast_backward']), linear_thrust['forward'])

    escape_linear4 = ctrl.Rule(distance_net_front['equal'], linear_thrust['stop'])

    escape_linear5 = ctrl.Rule(distance_net_front['back_distance'] & ship_speed['fast_backward'], linear_thrust['stop'])
    escape_linear6 = ctrl.Rule(distance_net_front['back_distance'] & ship_speed['slow_backward'], linear_thrust['reverse'])
    escape_linear7 = ctrl.Rule(distance_net_front['back_distance'] & (ship_speed['still'] | ship_speed['slow_forward'] | ship_speed['fast_forward']), linear_thrust['reverse'])

    escape_linear_rules = [escape_linear1, 
                           escape_linear2, 
                           escape_linear3,
                           escape_linear4,
                           escape_linear5,
                           escape_linear6,
                           escape_linear7, 
                           ]

    escape_angular1 = ctrl.Rule(distance_net_right['right_distance'], angular_thrust['right'])
    escape_angular2 = ctrl.Rule(distance_net_right['left_distance'], angular_thrust['left'])
    escape_angular3 = ctrl.Rule(distance_net_right['equal'], angular_thrust['stop'])
    
    escape_angular_rules = [escape_angular1, escape_angular2, escape_angular3]

    # Attack Rules
    # attack_linear1 = ctrl.Rule()

    attack_angular1 = ctrl.Rule(target_angle_error['left'], angular_thrust['left'])
    attack_angular2 = ctrl.Rule(target_angle_error['right'], angular_thrust['right'])
    attack_angular3 = ctrl.Rule(target_angle_error['center'], angular_thrust['stop'])

    attack_angular_rules = [attack_angular1, attack_angular2, attack_angular3]

    danger1 = ctrl.Rule(
        closest_danger_front['close'] | closest_danger_back['close'] | closest_danger_left['close'] | closest_danger_right['close'],
        danger['yes'])
    danger2 = ctrl.Rule(
        closest_danger_front['far'] & closest_danger_back['far'] & closest_danger_left['far'] & closest_danger_right['far'],
        danger['no'])

    danger_rules = [danger1, danger2]

    fire1 = ctrl.Rule(target_angle_error['center'], fire_command['yes'])
    fire2 = ctrl.Rule(target_angle_error['left'] | target_angle_error['right'], fire_command['no'])

    fire_rules = [fire1, fire2]

    # Control systems and simulators
    danger_ctrl = ctrl.ControlSystem(danger_rules)
    danger_sim = ctrl.ControlSystemSimulation(danger_ctrl)

    escape_linear_ctrl = ctrl.ControlSystem(escape_linear_rules)
    escape_linear_sim = ctrl.ControlSystemSimulation(escape_linear_ctrl)

    escape_angular_ctrl = ctrl.ControlSystem(escape_angular_rules)
    escape_angular_sim = ctrl.ControlSystemSimulation(escape_angular_ctrl)

    # attack_linear_ctrl = ctrl.ControlSystem(attack_linear_rules)
    # attack_linear_sim = ctrl.ControlSystemSimulation(attack_linear_ctrl)
    attack_linear_sim = None

    attack_angular_ctrl = ctrl.ControlSystem(attack_angular_rules)
    attack_angular_sim = ctrl.ControlSystemSimulation(attack_angular_ctrl)

    fire_ctrl = ctrl.ControlSystem(fire_rules)
    fire_sim = ctrl.ControlSystemSimulation(fire_ctrl)


    sims = Sims(
        danger_sim,
        fire_sim,
        attack_linear_sim,
        attack_angular_sim,
        escape_linear_sim,
        escape_angular_sim
        )

    return sims


class DangerFuzzy(KesslerController):
    def __init__(self,):
        """
        Any variables or initialization desired for the controller can be set up here
        """
        sims = create_fuzzy_system()
        self.sims = sims


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

        self.update_derived_features(ship_state, game_state)

        command = self.get_command()

        return command

    def get_command(self) -> tuple[float]:
        danger_sim = self.sims.danger_sim    
        fire_sim = self.sims.fire_sim
        escape_angular_sim = self.sims.escape_angular_sim
        escape_linear_sim = self.sims.escape_linear_sim
        attack_angular_sim = self.sims.attack_angular_sim
        # attack_linear_sim = self.sims.attack_linear_sim

        close_max = 1000
        angle_max = 180
        net_close_max = 200
        max_speed = 100

        num = np.clip(self.closest_danger_front, 0, close_max)/close_max
        print(f'danger front {num}')
        danger_sim.input['closest_danger_front'] = num
        num = np.clip(self.closest_danger_back, 0, close_max)/close_max
        print(f'danger back {num}')
        danger_sim.input['closest_danger_back'] = num
        num = np.clip(self.closest_danger_left, 0, close_max)/close_max
        print(f'danger left {num}')
        danger_sim.input['closest_danger_left'] = num
        num = np.clip(self.closest_danger_right, 0, close_max)/close_max
        print(f'danger right {num}')
        danger_sim.input['closest_danger_right'] = num
        
        fire_sim.input['target_angle_error'] = np.clip(self.target_angle_error, 0, angle_max)/angle_max

        danger_sim.compute()
        fire_sim.compute()

        # fire_command = fire_sim.output['fire_command']
        fire_command = False
        # danger = danger_sim.output['danger']
        danger = 1

        if self.in_danger(danger):

            num = np.clip(self.ship_speed, -max_speed, max_speed)/max_speed
            print(f'speed is num {num}')
            escape_linear_sim.input['ship_speed'] = num
            num = np.clip(self.distance_net_front, -net_close_max, net_close_max)/net_close_max
            print(f'diff front close {num}')
            escape_linear_sim.input['distance_net_front'] = num
            
            num = np.clip(self.distance_net_right, -net_close_max, net_close_max)/net_close_max
            print(f'diff right close {num}')
            escape_angular_sim.input['distance_net_right'] = num

            escape_linear_sim.compute()
            escape_angular_sim.compute()

            linear_thrust = escape_linear_sim.output['linear_thrust']
            angular_thrust = escape_angular_sim.output['angular_thrust']
        else:
            attack_angular_sim.input['target_angle_error'] = np.clip(self.target_angle_error, -angle_max, angle_max)/angle_max

            attack_angular_sim.compute()
            
            linear_thrust = 0
            angular_thrust = attack_angular_sim.output['angular_thrust']

        scale1 = 500
        scale2 = 1000
        scale3 = 100

        print(f"linear thrust is {linear_thrust} or {scale1 * linear_thrust}")

        command = (scale1 * linear_thrust, scale2 * angular_thrust, scale3 * fire_command)
        print(f'Danger is: {self.in_danger(danger)}')
        print(command)

        return command
    
    def get_closest_asteroid(self, ship_state: Dict, game_state: Dict) -> Asteroid.state:
        closest_distance = 1000000
        closest_state = None

        my_position = ship_state['position']
        my_position = np.array(my_position)

        for asteroid_state in game_state['asteroids']:
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

        map_size = game_state['map_size']

        ship_heading = ship_state['heading']
        ship_angle = 90 - ship_heading

        pairs = []

        for asteroid_state in game_state['asteroids']:
            d_vec = np.array(ship_state['position']) - np.array(asteroid_state['position'])
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
            

    def update_derived_features(self, ship_state: Dict, game_state: Dict) -> None:
        '''
        Update all of the following derived features:

        target_angle_error
        # closest_target_distance
        # closest_target_angle
        # closest_target_velocity
        # closest_target_trajectory
        closest_danger_front
        closest_danger_back
        closest_danger_left
        closest_danger_right
        '''

        self.update_target_angle_error(ship_state, game_state)
        # self.update_closest_target_distance()
        # self.update_closest_target_angle()
        # self.update_closest_target_velocity()
        # self.update_closest_target_trajectory()
        self.update_closest_danger_front(ship_state, game_state)
        self.update_closest_danger_back(ship_state, game_state)
        self.update_closest_danger_left(ship_state, game_state)
        self.update_closest_danger_right(ship_state, game_state)
        self.update_distance_net_front(ship_state, game_state)
        self.update_distance_net_right(ship_state, game_state)
        self.update_ship_velocity(ship_state, game_state)

    def update_target_angle_error(self, ship_state: Dict, game_state: Dict) -> None:
        closest_asteroid = self.get_closest_asteroid(ship_state, game_state)

        my_angle = ship_state['heading']

        relative_position = np.array(closest_asteroid['position']) - np.array(ship_state['position'])
        set_point_angle = np.arctan2(relative_position[1], relative_position[0])
        set_point_angle = np.rad2deg(set_point_angle)

        error = (my_angle - set_point_angle) % 360
        if error > 180:
            error -= 360

        self.target_angle_error = -error

    # def update_closest_target_distance(self, ship_state: Dict, game_state: Dict) -> None:
    #     # TODO
    #     pass

    # def update_closest_target_angle(self, ship_state: Dict, game_state: Dict) -> None:
    #     # TODO
    #     pass

    # def update_closest_target_velocity(self, ship_state: Dict, game_state: Dict) -> None:
    #     # TODO
    #     pass

    # def update_closest_target_trajectory(self, ship_state: Dict, game_state: Dict) -> None:
    #     # TODO
    #     pass

    def update_closest_danger_front(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = -1

        for distance, angle in asteroid_distance_angles:
            if (angle <= 115 and angle >= 45) and (distance < closest or closest == -1):
                closest = distance
        
        self.closest_danger_front = closest


    def update_closest_danger_back(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = -1

        for distance, angle in asteroid_distance_angles:
            if (angle <= -45 and angle >= -135) and (distance < closest or closest == -1):
                closest = distance
        
        self.closest_danger_back = closest

    def update_closest_danger_left(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = -1

        for distance, angle in asteroid_distance_angles:
            if (angle <= -135 or angle >= 135) and (distance < closest or closest == -1):
                closest = distance
        
        self.closest_danger_left = closest

    def update_closest_danger_right(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = -1

        for distance, angle in asteroid_distance_angles:
            if (angle <= 45 and angle >= -45) and (distance < closest or closest == -1):
                closest = distance
        
        self.closest_danger_right = closest

    def update_distance_net_front(self, ship_state: Dict, game_state: Dict) -> None:
        front = self.closest_danger_front 
        back = self.closest_danger_back

        if front == -1:
            front = 0

        if back == -1:
            back = 0

        diff = front - back

        self.distance_net_front = diff

    def update_distance_net_right(self, ship_state: Dict, game_state: Dict) -> None:
        right = self.closest_danger_right 
        left = self.closest_danger_left

        if right == -1:
            right = 0

        if left == -1:
            left = 0

        diff = right - left

        self.distance_net_right = diff

    def in_danger(self, danger):
        threshold = 0.5
        return danger > threshold

    def update_ship_velocity(self, ship_state: Dict, game_state: Dict) -> None:
        speed = ship_state['speed']
        self.ship_speed = speed

    @property
    def name(self) -> str:
        """
        Simple property used for naming controllers such that it can be displayed in the graphics engine

        Returns:
            str: name of this controller
        """
        return "Fuzzy Tree Controller"
