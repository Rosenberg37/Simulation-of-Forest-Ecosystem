from matplotlib import pyplot as plt

import config
from modules.biomass import Biomass
from modules.products import Products
from modules.soil import Soil


class Stimulator:
    def __init__(self, biomass_config: list[dict], soil_config: dict, products_config: dict):
        self.biomass = Biomass(biomass_config)
        self.soil = Soil(**soil_config)
        self.products = Products(**products_config)

    def __call__(self):
        material, turnover = self.biomass()
        self.soil(**turnover)
        self.products(**material)

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.__dict__.values()))


if __name__ == '__main__':
    sim = Stimulator(config.BIOMASS_CONFIG, config.SOIL_CONFIG, config.PRODUCTS_CONFIG)
    years = list(range(500))
    total_carbon, biomass_carbon, soil_carbon, products_carbon = list(), list(), list(), list()

    for i in years:
        total_carbon.append(sim.carbon)
        biomass_carbon.append(sim.biomass.carbon)
        soil_carbon.append(sim.soil.carbon)
        products_carbon.append(sim.products.carbon)
        sim()
    plt.plot(years, total_carbon, label='total')
    plt.plot(years, biomass_carbon, label='biomass')
    plt.plot(years, soil_carbon, label='soil')
    plt.plot(years, products_carbon, label='soil')
    plt.show()
