import matplotlib.pyplot as plt
import numpy as np
from .evo_simulation import EvoWorldSimulation

def life_expectancy(evo_simulation: EvoWorldSimulation):
    evo_simulation.reset()
    evo_simulation.run()
    entities = map(lambda x: x[2], evo_simulation.banished_entities)
    species_info:dict[str, dict[str,int]] = {}
    for entity in entities:
        species_info.setdefault(entity.species, {})
        species_info[entity.species].setdefault("ages", 0)
        species_info[entity.species].setdefault("count", 0)
        species_info[entity.species]["ages"] += entity.age
        species_info[entity.species]["count"] += 1
    specie_life_mean = {}
    for specie, info in species_info.items():
        specie_life_mean[specie] = info["ages"] / info["count"]
    return specie_life_mean

def plot_species_count_over_time(evo_simulation: EvoWorldSimulation):
    history = evo_simulation.get_history()
    species = set()
    for episode in history:
        for step in episode:
            for specie in step.keys():
                species.add(specie)
    species = list(species)
    species.sort()
    species_count = np.zeros((len(history), len(species)))
    for episode_index, episode in enumerate(history):
        for step_index, step in enumerate(episode):
            for specie_index, specie in enumerate(species):
                species_count[episode_index][specie_index] += step.get(specie, 0)
    for specie_index, specie in enumerate(species):
        plt.plot(species_count[:, specie_index], label=specie)
    plt.legend()
    plt.show()

def plot_life_expectancy(evo_simulation: EvoWorldSimulation):
    life_expectancy_dict = life_expectancy(evo_simulation)
    plt.bar(life_expectancy_dict.keys(), life_expectancy_dict.values())
    plt.show()
