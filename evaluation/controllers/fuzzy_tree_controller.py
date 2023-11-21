from typing import Dict, Tuple

import numpy as np

import skfuzzy as fuzz
from skfuzzy import control as ctrl

from kesslergame import KesslerController
from kesslergame.asteroid import Asteroid
from kesslergame.ship import Ship

def create_fuzzy_system() -> tuple:

    # Antecedents
    target_angle_error = ctrl.Antecedent(np.linspace(-1, 1, 100), 'target_angle_error')
    # closest_target_distance = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_target_distance')
    # closest_target_angle = ctrl.Antecedent(np.linspace(-1, 1, 100), 'closest_target_angle')
    # closest_target_velocity = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_target_velocity')
    # closest_target_trajectory = ctrl.Antecedent(np.linspace(-1, 1, 100), 'closest_target_trajectory') # NOTE maybe just trajectory - my heading? simpler?
    closest_danger_front = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_front')
    closest_danger_back = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_back')
    closest_danger_left = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_left')
    closest_danger_right = ctrl.Antecedent(np.linspace(0, 1, 100), 'closest_danger_right')
    distance_net_front = ctrl.Antecedent(np.linspace(-1, 1, 100), 'distance_net_front')

    # Both Antecedent AND Consequent
    in_danger_A = ctrl.Antecedent(np.linspace(0, 1, 100), 'in_danger_A')
    in_danger_C = ctrl.Consequent(np.linspace(0, 1, 100), 'in_danger_C')

    # Consequents
    linear_thrust = ctrl.Consequent(np.linspace(-1, 1, 100), 'linear_thrust')
    angular_thrust = ctrl.Consequent(np.linspace(-1, 1, 100), 'angular_thrust')
    fire_command = ctrl.Consequent(np.linspace(-1, 1, 100), 'fire_command')

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

    in_danger_A['no'] = fuzz.trimf(in_danger_A.universe, (0, 0, 0.5))
    in_danger_A['yes'] = fuzz.trimf(in_danger_A.universe, (0, 1, 1))

    in_danger_C['no'] = fuzz.trimf(in_danger_C.universe, (0, 0, 1))
    in_danger_C['yes'] = fuzz.trimf(in_danger_C.universe, (0, 1, 1))

    linear_thrust['reverse'] = fuzz.trimf(linear_thrust.universe, (-1, -1, 0))
    linear_thrust['stop'] = fuzz.trimf(linear_thrust.universe, (-1, 0, 1))
    linear_thrust['forward'] = fuzz.trimf(linear_thrust.universe, (0, 1, 1))

    angular_thrust['left'] = fuzz.trimf(angular_thrust.universe, (-1, -1, 0))
    angular_thrust['stop'] = fuzz.trimf(angular_thrust.universe, (-1, 0, 1))
    angular_thrust['right'] = fuzz.trimf(angular_thrust.universe, (0, 1, 1))

    fire_command['no'] = fuzz.trimf(fire_command.universe, (0, 0, 1))
    fire_command['yes'] = fuzz.trimf(fire_command.universe, (0, 1, 1))

    # Rules
    # linear1 = ctrl.Rule(in_danger_A['yes'] & closest_danger_front['close'], linear_thrust['reverse'])
    # linear2 = ctrl.Rule(in_danger_A['yes'] & closest_danger_back['close'], linear_thrust['forward'])
    linear4 = ctrl.Rule(in_danger_A['yes'] & distance_net_front['front_distance'], linear_thrust['forward'])
    linear5 = ctrl.Rule(in_danger_A['yes'] & distance_net_front['equal'], linear_thrust['stop'])
    linear6 = ctrl.Rule(in_danger_A['yes'] & distance_net_front['back_distance'], linear_thrust['reverse'])
    linear3 = ctrl.Rule(in_danger_A['no'], linear_thrust['stop'])

    linear_rules = [linear4, linear5, linear6, linear3]

    angular1 = ctrl.Rule(target_angle_error['left'] & in_danger_A['no'], angular_thrust['left'])
    angular2 = ctrl.Rule(target_angle_error['right'] & in_danger_A['no'], angular_thrust['right'])
    angular3 = ctrl.Rule(target_angle_error['center'] & in_danger_A['no'], angular_thrust['stop'])
    angular4 = ctrl.Rule(in_danger_A['yes'] & closest_danger_left['close'], angular_thrust['right'])
    angular5 = ctrl.Rule(in_danger_A['yes'] & closest_danger_right['close'], angular_thrust['left'])

    angular_rules = [angular1, angular2, angular3, angular4, angular5]

    danger1 = ctrl.Rule(
        closest_danger_front['close'] | closest_danger_back['close'] | closest_danger_left['close'] | closest_danger_right['close'],
        in_danger_C['yes'])
    danger2 = ctrl.Rule(
        closest_danger_front['far'] & closest_danger_back['far'] & closest_danger_left['far'] & closest_danger_right['far'],
        in_danger_C['no'])

    danger_rules = [danger1, danger2]

    fire1 = ctrl.Rule(target_angle_error['center'], fire_command['yes'])
    fire2 = ctrl.Rule(target_angle_error['left'] | target_angle_error['right'], fire_command['no'])

    fire_rules = [fire1, fire2]

    # Control systems and simulators
    danger_ctrl = ctrl.ControlSystem(danger_rules)
    danger_sim = ctrl.ControlSystemSimulation(danger_ctrl)

    linear_ctrl = ctrl.ControlSystem(linear_rules)
    linear_sim = ctrl.ControlSystemSimulation(linear_ctrl)

    angular_ctrl = ctrl.ControlSystem(angular_rules)
    angular_sim = ctrl.ControlSystemSimulation(angular_ctrl)

    fire_ctrl = ctrl.ControlSystem(fire_rules)
    fire_sim = ctrl.ControlSystemSimulation(fire_ctrl)

    return danger_sim, linear_sim, angular_sim, fire_sim


class FuzzyController(KesslerController):
    def __init__(self,):
        """
        Any variables or initialization desired for the controller can be set up here
        """

        danger_sim, linear_sim, angular_sim, fire_sim = create_fuzzy_system()


        self.danger_sim = danger_sim
        self.linear_sim = linear_sim
        self.angular_sim = angular_sim
        self.fire_sim = fire_sim


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

    def get_command(self) -> float:
        danger_sim = self.danger_sim    
        fire_sim = self.fire_sim
        linear_sim = self.linear_sim
        angular_sim = self.angular_sim

        close_max = 1000
        angle_max = 180
        net_close_max = 100

        danger_sim.input['closest_danger_front'] = np.clip(self.closest_danger_front, 0, close_max)/close_max
        danger_sim.input['closest_danger_back'] = np.clip(self.closest_danger_back, 0, close_max)/close_max
        danger_sim.input['closest_danger_left'] = np.clip(self.closest_danger_left, 0, close_max)/close_max
        danger_sim.input['closest_danger_right'] = np.clip(self.closest_danger_right, 0, close_max)/close_max
        
        fire_sim.input['target_angle_error'] = np.clip(self.target_angle_error, 0, angle_max)/angle_max

        danger_sim.compute()
        fire_sim.compute()

        in_danger = danger_sim.output['in_danger_C']
        fire_command = fire_sim.output['fire_command']

        linear_sim.input['in_danger_A'] = in_danger
        linear_sim.input['distance_net_front'] = np.clip(self.distance_net_front, -net_close_max, net_close_max)/net_close_max
        # linear_sim.input['closest_danger_front'] = np.clip(self.closest_danger_front, 0, close_max)/close_max
        # linear_sim.input['closest_danger_back'] = np.clip(self.closest_danger_back, 0, close_max)/close_max

        # print(f'front is {self.closest_danger_front}')
        # print(f'back is {self.closest_danger_back}')
        # print(f'in_danger is {in_danger}')
        # print(f'net_front is {self.distance_net_front}')
        # print(f'dumb {np.clip(self.distance_net_front, -net_close_max, net_close_max)/net_close_max}')

        angular_sim.input['in_danger_A'] = in_danger
        angular_sim.input['target_angle_error'] = np.clip(self.target_angle_error, -angle_max, angle_max)/angle_max
        angular_sim.input['closest_danger_left'] = np.clip(self.closest_danger_left, 0, close_max)/close_max
        angular_sim.input['closest_danger_right'] = np.clip(self.closest_danger_right, 0, close_max)/close_max

        linear_sim.compute()
        angular_sim.compute()

        linear_thrust = linear_sim.output['linear_thrust']
        angular_thrust = angular_sim.output['angular_thrust']

        # print(f'angle error {self.target_angle_error}')

        scale1 = 250
        scale2 = 1000
        scale3 = 100

        # print(f"commands: {(linear_thrust, angular_thrust, fire_command)}")

        return scale1 * linear_thrust, scale2 * angular_thrust, scale3 * fire_command
    
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
        
        closest = 1000000

        for distance, angle in asteroid_distance_angles:
            if (angle <= 115 and angle >= 45) and distance < closest:
                closest = distance
        
        self.closest_danger_front = closest


    def update_closest_danger_back(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = 1000000

        for distance, angle in asteroid_distance_angles:
            if (angle <= -45 and angle >= -135) and distance < closest:
                closest = distance
        
        self.closest_danger_back = closest

    def update_closest_danger_left(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = 1000000

        for distance, angle in asteroid_distance_angles:
            if (angle <= -135 or angle >= 135) and distance < closest:
                closest = distance
        
        self.closest_danger_left = closest

    def update_closest_danger_right(self, ship_state: Dict, game_state: Dict) -> None:
        asteroid_distance_angles = self.get_asteroid_distance_angles(ship_state, game_state)
        
        closest = 1000000

        for distance, angle in asteroid_distance_angles:
            if (angle <= 45 and angle >= -45) and distance < closest:
                closest = distance
        
        self.closest_danger_right = closest

    def update_distance_net_front(self, ship_state: Dict, game_state: Dict) -> None:
        self.distance_net_front = self.closest_danger_front - self.closest_danger_back


    @property
    def name(self) -> str:
        """
        Simple property used for naming controllers such that it can be displayed in the graphics engine

        Returns:
            str: name of this controller
        """
        return "Fuzzy Tree Controller"
