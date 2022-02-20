from sko.GA import GA
from tqdm import tqdm

import config
from modules import Stimulator

bar = tqdm()


def optim(fraction: list):
    configs = config.BIOMASS_CONFIG, config.SOIL_CONFIG, config.PRODUCTS_CONFIG
    configs[0]['pine']['thinning_harvest_dict']['fraction'] = fraction
    stimulator = Stimulator(*configs)
    stimulator(100)
    bar.update()
    return -stimulator.carbon


if __name__ == '__main__':
    years = config.OPTIM_OPTIONS['years']
    ga = GA(
        func=optim,
        n_dim=years,
        max_iter=config.OPTIM_OPTIONS['max_iter'],
        lb=[0] * years,
        ub=[1] * years
    )
    best_x, best_y = ga.run()
    print('best_fraction', best_x, '\n', 'max_carbon:', -best_y)
