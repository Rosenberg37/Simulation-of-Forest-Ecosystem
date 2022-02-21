from sko.GA import GA
from tqdm import tqdm

import config
from modules import Stimulator

bar = tqdm()


def optim(fraction: list):
    configs = config.BIOMASS_CONFIG, config.SOIL_CONFIG, config.PRODUCTS_CONFIG
    configs[0]['pine']['thinning_harvest_dict']['fraction'] = fraction
    stimulator = Stimulator(*configs)
    stimulator(config.OPTIM_OPTIONS['simulate_year'])
    bar.update()
    total = stimulator.carbon_table['total']
    return -sum(total) / len(total)


if __name__ == '__main__':
    times = config.OPTIM_OPTIONS['harvest_times']
    ga = GA(
        func=optim,
        n_dim=times,
        max_iter=config.OPTIM_OPTIONS['max_iter'],
        lb=[0] * times,
        ub=[1] * times
    )
    best_x, best_y = ga.run()
    print('best_fraction', best_x, '\n', 'max_carbon:', -best_y)
