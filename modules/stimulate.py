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

        self.carbon_table = list()
        self.biomass_table = list()

    def __call__(self, years):
        for i in range(years):
            self.iterate()

    def iterate(self):
        material, turnovers = self.modules['biomass']()
        self.modules['soil'](turnovers)
        self.modules['products'](**material)

        self.carbon_table.append(self.carbon)
        self.biomass_table.append(self.modules['biomass'].biomass)

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.modules.values()))


if __name__ == '__main__':
    sim = Stimulator(config.BIOMASS_CONFIG, config.SOIL_CONFIG, config.PRODUCTS_CONFIG)
    years = list(range(100))
    total_carbon, biomass_carbon, soil_carbon, products_carbon = list(), list(), list(), list()

    for i in years:
        total_carbon.append(sim.carbon)
        biomass_carbon.append(sim.biomass.carbon)
        soil_carbon.append(sim.soil.carbon)
        products_carbon.append(sim.products.carbon)
        sim.iterate()
    plt.plot(years, total_carbon, color='yellow')
    plt.plot(years, biomass_carbon, color='red')
    plt.plot(years, soil_carbon, color='green')
    plt.plot(years, products_carbon, color='blue')
    plt.show()
