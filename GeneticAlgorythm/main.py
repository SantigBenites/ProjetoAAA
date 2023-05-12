import random
from itertools import *
import time
import math
import pandas as pd
import multiprocessing as mp
import matplotlib.pyplot as plt

from chess import Game
from ReiforcementLearning.RLplayer import Player
from moveGeneration import distance_to_edge
from pieces import genotype
from chessboard import Chessboard

POPULATION_SIZE = 30
MUTATION_PROB = 0.05
GAMES_NUMBER = 10

cb = Chessboard(
            [3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
             0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,
             3+16,5+16,4+16,2+16,1+16,4+16,5+16,3+16
            ],                      # set board
            [int(time.time())-10] * 64, # set current timestamps
            0               # set cooldown
        )

def genotype_intializer():
    def random_chromossome():
        return {chromossome: random.randint(0,5000) for chromossome in genotype.keys()}
    
    return [random_chromossome() for x in range(POPULATION_SIZE)]

def crossover_fuction(indeviduals : list[tuple]):

    # List of (genotype, fitness)
    # fenotypes = [indevidual[0] for indevidual in indeviduals]
    temp_genotypes = list(genotype.keys()).copy()
    starter_genotypes = []
    for i in range(0,math.floor(len(genotype.keys()) / 2)):
        gene = random.choice(temp_genotypes)
        starter_genotypes.append(gene)
        temp_genotypes.remove(gene)

    ender_genotype = temp_genotypes


    starts = []
    ends = []
    for indevidual_genotype in indeviduals:

        first_half_genotype = {}
        second_half_genotype = {}
        for chromo in indevidual_genotype.keys():
            if chromo in starter_genotypes:
                first_half_genotype[chromo] = indevidual_genotype[chromo]
            else:
                second_half_genotype[chromo] = indevidual_genotype[chromo]

        starts.append(first_half_genotype)
        ends.append(second_half_genotype)

    newChromo = []

    for chromo in range(0,POPULATION_SIZE):
        start = random.choice(starts)
        end = random.choice(ends)

        newChromo.append(start | end)

    #keys, values = zip(*combined.items())
    #permutations_dicts = [dict(zip(keys, v)) for v in product(*values)]
    #return random.sample(permutations_dicts, POPULATION_SIZE)
    return newChromo

def fitness(results: list[tuple[dict[str, int], int]]):
    fitnesses: dict[dict[str, int], int] = dict()
    #*                    ^genotipo      ^fitness desse genotypo
    
    for res in results:

        if fitnesses.get(tuple(res[0].items()), None) == None:
            fitnesses[tuple(res[0].items())] = 0
        fitnesses[tuple(res[0].items())] += res[1]
        
    return fitnesses

def ordered_to_dict(results):
    
    # ((('PAWN_VALUE', 1949), ('KNIGHT_VALUE', 3019), ('BISHOP_VALUE', 4448), ('ROOK_VALUE', 4690), ('QUEEN_VALUE', 3976), ('KING_CAPTURE', 4138), ('INFRONT_VALUE', 2522), ('KING_LOSS', 2452), ('KING_ATACK', 2910), ('QUEEN_ATACK', 484), ('CAPTURE_VALUE', 74), ('EDGE_VALUE', 719)), 8),
    #print(f"{results} ordered_to_dict")
    res: list[tuple[dict[str , int], int]] = []
    #*          ^genotipo      ^fitness desse genotypo
    
    for genotuple in results:
        genotype = dict()
        for tuople in genotuple:
            genotype[tuople[0]] = tuople[1]
        
        res.append(genotype)
    
    return res
    pass
    

if __name__ == '__main__':
    
    distance_to_edge()
    iterations = 0
    dataframe_dict = {"X" : [], "Y1" : [], "Y2" : []}
    
    best_fitnesses = []
    
    population = genotype_intializer() 
        
    while population and iterations < 8:

        #whites = population[::2]
        #blacks = population[1::2]
        #? [whites.append(ind) if count % 2 == 0 else blacks.append(ind) for count,ind in enumerate(population)]

        # pões a jogar uns contra os outros ao calhas
        #random.shuffle(whites)
        #random.shuffle(blacks)
        #player_pairs = zip(whites,blacks)

        player_pairs = []
        for count, x in enumerate(population):
            possible_oponents = [x for i,x in enumerate(population) if i!=count]
            for number_game in range(0, GAMES_NUMBER):
                player_pairs.append((x, random.choice(possible_oponents)))
        
        def task(geno1, geno2):
            g = Game(cooldown=4, geno_1=geno1, geno_2=geno2)
            return g.play()
        
        results = []
        
        with mp.Pool() as pool:
            results = pool.starmap(task, player_pairs)
            
        results = [item for sublist in results for item in sublist]
        
        fitted_results = fitness(results)

        ordered_results = sorted(fitted_results.items(), key=lambda tup: tup[1])
        ordered_results.reverse()

        #print(f"{ordered_results}--- this ordered_results")
        

        best_fitnesses.append(ordered_results[0])
        
        dataframe_dict["X"].append(iterations)
        dataframe_dict["Y1"].append(ordered_results[0][1])
        dataframe_dict["Y2"].append(ordered_results[1][1])

        print(f"X - {dataframe_dict['X']}, Y1 - {dataframe_dict['Y1']} , Y2 - {dataframe_dict['Y2']}")

        # reproduzes
        # need to randomize list of genotypes
        ten_percent_best = ordered_results[0 : math.floor(0.30*len(ordered_results))]
        to_crossover = ordered_to_dict([x[0] for x in ten_percent_best])
        new_genotype_list = crossover_fuction(to_crossover)
        
        # mutas
        for geno in new_genotype_list:
            if random.random() < MUTATION_PROB:
                geno[random.choice(list(geno.keys()))] += random.choice(list(range(-1000, 1000, 50)))

        
        # substituicao
        population = []
        for count, geno in enumerate(new_genotype_list):
            population.append(geno) if count %2 == 0 else population.append(geno)  


        # repeat (fim do loop)
        iterations +=1
        print("End of iteration", iterations)

        pass

    df = pd.DataFrame(dataframe_dict)
    print(df.to_string())
    print(best_fitnesses)

