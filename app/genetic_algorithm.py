# app/genetic_algorithm.py
import random
import numpy as np
from deap import base, creator, tools, algorithms

def evaluate(individual, data):
    short_window = individual[0]
    long_window = individual[1]
    rsi_threshold = individual[2]

    data['ma_short'] = data['close'].rolling(window=short_window).mean()
    data['ma_long'] = data['close'].rolling(window=long_window).mean()
    data['signal'] = 0
    data['signal'] = np.where(data['ma_short'] > data['ma_long'], 1, -1)
    data['positions'] = np.where(data['rsi'] < rsi_threshold, data['signal'], 0)
    data['strategy_returns'] = data['positions'].shift(1) * data['close'].pct_change()
    total_return = data['strategy_returns'].cumsum().iloc[-1]
    return (total_return,)

def run_ga(data):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_short_window", random.randint, 5, 20)
    toolbox.register("attr_long_window", random.randint, 21, 100)
    toolbox.register("attr_rsi_threshold", random.randint, 30, 70)
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (toolbox.attr_short_window, toolbox.attr_long_window, toolbox.attr_rsi_threshold), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, data=data)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", tools.mutUniformInt, low=[5,21,30], up=[20,100,70], indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=50)
    NGEN = 10

    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        best_ind = tools.selBest(population, k=1)[0]
        print(f"Generation {gen}: Best Fitness = {best_ind.fitness.values[0]}")

    best_ind = tools.selBest(population, k=1)[0]
    return best_ind
