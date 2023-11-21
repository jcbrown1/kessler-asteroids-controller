# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.

from kesslergame import KesslerController
from typing import Dict, Tuple
from kesslergame.asteroid import Asteroid
from kesslergame.ship import Ship
from kesslergame.bullet import Bullet
import numpy as np
from scipy.optimize import fsolve


class BasicController(KesslerController):
    def __init__(self):
        """
        Any variables or initialization desired for the controller can be set up here
        """
        ...

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
            bool: mine deployment control value. Lays mine if true
        """

        thrust = self.get_thrust(ship_state, game_state)
        turn_rate = self.get_turn_rate(ship_state, game_state)
        fire = True
        # drop_mine = False

        

        # return thrust, turn_rate, fire, drop_mine  # not using V2?
        return thrust, turn_rate, fire

    def get_turn_rate(self, ship_state: Dict, game_state: Dict):
        # determine what the turn rate should be.
        # For now, it will be based on trying to shoot the closest asteroid
        
        closest_asteroid = get_closest_asteroid(ship_state['position'], game_state['asteroids'])
        turn_rate = turn_toward(ship_state, closest_asteroid)
        
        return turn_rate

    def get_thrust(self, ship_state: Dict, game_state: Dict):
        
        closest_asteroid = get_closest_asteroid(ship_state['position'], game_state['asteroids'])
        target_distance = 100
        # should not be closest asteroid, should actually be
        # closest asteroid in line of sight
        distance = np.linalg.norm(np.array(closest_asteroid['position']) - ship_state['position'])
        error = distance - target_distance
        weight = 1
        thrust = P_control(error, weight)
        max_thrust = 300
        thrust = np.clip(thrust, -max_thrust, max_thrust)

        return thrust


    @property
    def name(self) -> str:
        """
        Simple property used for naming controllers such that it can be displayed in the graphics engine

        Returns:
            str: name of this controller
        """
        return "Test Controller"

def get_closest_asteroid(my_position: tuple, asteroid_states: list[Asteroid.state]) -> Asteroid.state:
    closest_distance = -1
    closest_state = None

    my_position = np.array(my_position)

    for state in asteroid_states:
        their_position = np.array(state['position'])
        vector_diff = np.array(my_position - their_position)
        distance_diff = np.linalg.norm(vector_diff) - state['size']
        
        if closest_distance == -1 or closest_distance > distance_diff:
            closest_distance = distance_diff
            closest_state = state

    return closest_state


def turn_toward(my_state: Ship.state, asteroid_state: Asteroid.state) -> float:
    # Determine angular turn rate so that we can turn toward the target asteroid
    # Implement a simple P controller around the set point
    my_angle = my_state['heading']
    relative_position = np.array(asteroid_state['position']) - np.array(my_state['position'])

    set_point_angle = look_ahead(asteroid_state['position'], asteroid_state['velocity'], my_state['position'], 800)

    # set_point_angle = np.arctan2(relative_position[1], relative_position[0])
    # set_point_angle = np.rad2deg(set_point_angle)

    error = (my_angle - set_point_angle) % 360
    if error > 180:
        error -= 360
    print(f"relative_positon is {relative_position}")
    print(f"set_point_angle is {set_point_angle}")
    print(f"my_angle is {my_angle}")
    print(f"error is {error}")
    weight = 50
    turn_rate = P_control(error, weight)
    max_turn = 1000
    turn_rate = np.clip(turn_rate, -max_turn, max_turn) 

    return turn_rate


def P_control(error: float, weight: float) -> float:
    # Basic P controller
    return - weight * error


def look_ahead(target_position, target_velocity, my_position, bullet_velocity) -> np.ndarray:
    # Mathematical intersection point
    # This assumes I am able to move instantly to the target, so this could be
    # where the AI comes in to tune some values for how to lead the bullet even more.
    dx = target_position[0] - my_position[0]
    dy = target_position[1] - my_position[1]

    term1 = lambda angle : (-dx) * (bullet_velocity * np.sin(np.deg2rad(angle)) - target_velocity[1])
    term2 = lambda angle : (-dy) * (bullet_velocity * np.cos(np.deg2rad(angle)) - target_velocity[0])
    equation = lambda angle : term1(angle) - term2(angle)
    shoot_angle = fsolve(equation, 0)
    shoot_angle = shoot_angle[0]

    if dx < 0:
        shoot_angle += 180

    return shoot_angle