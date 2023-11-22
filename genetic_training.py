import random
import EasyGA as ega
from evaluation.controller_scorer import evaluate_controller

def gen_gene():
    gene = random.random()
    return gene




ga = ega.GA()

ga.chromosome_length = 3 * 9

ga.target_fitness_type = 'min'
ga.fitness_goal = 0

ga.population_size = 5
ga.generation_goal = 40

ga.gene_impl = gen_gene
ga.fitness_function_impl = evaluate_controller

ga.evolve()

