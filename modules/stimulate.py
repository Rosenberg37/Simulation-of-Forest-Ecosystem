from matplotlib import pyplot as plt

import config
from modules.biomass import Biomass
from modules.products import Products
from modules.soil import Soil


class Stimulator:
    def __init__(self, biomass_config: dict, soil_config: dict, products_config: dict):
        self.modules = {
            'biomass': Biomass(biomass_config),
            'soil': Soil(**soil_config),
            'products': Products(**products_config)
        }

        self.carbon_table = {
            'biomass': list(),
            'soil': list(),
            'products': list(),
            'total': list(),
        }
        self.biomass_table = list()

    def __call__(self, years):
        for i in range(years):
            self.iterate()

    def iterate(self):
        material, turnovers = self.modules['biomass']()
        self.modules['soil'](turnovers)
        self.modules['products'](**material)

        self.carbon_table['total'].append(self.carbon)
        for key in ['soil', 'products', 'biomass']:
            self.carbon_table[key].append(self.modules[key].carbon)
        self.biomass_table.append(self.modules['biomass'].biomass)

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.modules.values()))


if __name__ == '__main__':
    simulate = Stimulator(config.BIOMASS_CONFIG, config.SOIL_CONFIG, config.PRODUCTS_CONFIG)
    years = 100
    x = list(range(years))
    total_carbon, biomass_carbon, soil_carbon, products_carbon = list(), list(), list(), list()

    simulate(years)
    plt.plot(x, simulate.carbon_table['total'], color='yellow')
    plt.plot(x, simulate.carbon_table['biomass'], color='red')
    plt.plot(x, simulate.carbon_table['soil'], color='green')
    plt.plot(x, simulate.carbon_table['products'], color='blue')
    plt.show()
