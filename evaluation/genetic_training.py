import random
import EasyGA as ega
from controller_scorer import evaluate_chromosome
# import mpu

def gen_gene():
    gene = random.random()
    return gene


ga = ega.GA()

ga.chromosome_length = 3

ga.target_fitness_type = 'max'
ga.fitness_goal = 300

ga.population_size = 3
ga.generation_goal = 5

ga.gene_impl = gen_gene
ga.fitness_function_impl = evaluate_chromosome

ga.evolve()

ga.print_best_chromosome()

# mpu.io.write('trained.pickle', ga)