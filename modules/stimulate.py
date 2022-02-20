from matplotlib import pyplot as plt

import config
from modules.biomass import Biomass
from modules.soil import Soil


class Stimulator:
    def __init__(self, biomass_config: list[dict], soil_config: dict):
        self.biomass = Biomass(biomass_config)
        self.soil = Soil(**soil_config)

    def __call__(self):
        _, turnover = self.biomass()
        self.soil(**turnover)

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.__dict__.values()))


if __name__ == '__main__':
    module = Stimulator(config.BIOMASS_CONFIG, config.SOIL_CONFIG)
    years, carbon = list(range(500)), list()
    for i in years:
        carbon.append(module.carbon)
        print(f"Year:{i},"
              f"Carbon:{module.carbon}")
        module()
    plt.plot(years, carbon)
    plt.show()
