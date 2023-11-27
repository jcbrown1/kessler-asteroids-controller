from typing import Dict, Tuple

import numpy as np

import skfuzzy as fuzz
from skfuzzy import control as ctrl

from kesslergame import KesslerController
from kesslergame.asteroid import Asteroid
from controllers.simple_fuzzy import SimpleFuzzy, create_fuzzy_system


class GeneticFuzzy(SimpleFuzzy):
    def __init__(self, values):
        """
        Any variables or initialization desired for the controller can be set up here
        """
        sim = create_fuzzy_system()
        self.sim = sim

        self.target_distance = remap(get(values, 1), 150, 250)
        self.angle_max = 180
        self.max_speed = remap(get(values, 1), 350, 500)

        self.linear_scaling = remap(get(values, 1), 400, 550)
        self.angular_scaling = remap(get(values, 1), 450, 550)
        self.eval_frames = 0  # required field in scenario test
        

    @property
    def name(self) -> str:
        """
        Simple property used for naming controllers such that it can be displayed in the graphics engine

        Returns:
            str: name of this controller
        """
        return "Genetic Fuzzy"

def normalize(num, mx, symmetric=False):
    if symmetric:
        mn = -mx
    else:
        mn = 0
    
    normal = np.clip(num, mn, mx) / mx
    return normal

def genetic_controller(chromosome=False):
    if chromosome is False:
        # Use best values:
        values = [0.80857, 0.76046, 0.922634, 0.755019]
    else:
        values = []
        for gene in chromosome:
            values.append(gene.value)
            
    controller = GeneticFuzzy(values)

    return controller

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