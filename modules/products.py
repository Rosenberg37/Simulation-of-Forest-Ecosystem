import math

from matplotlib import pyplot as plt

import config


class EndProducts:
    factor = math.log(2)

    def __init__(self, allocation: dict, end_of_life: dict, recycle: dict, life_span: dict, products: dict):
        self.life_span = life_span
        self.recycle = recycle
        self.end_of_life = end_of_life
        self.allocation = allocation
        self.products = products

    def __call__(self, commodities: dict):
        delta = dict(map(lambda a: (a, 0), self.products.keys()))

        delta['mile_site_dump'] += commodities.pop('mile_site_dump')
        for key, value in commodities.items():
            for k, v in self.allocation[key].items():
                delta[k] += v * value

        for key in ['long', 'medium', 'short']:
            remove = self.products[key] * self.factor / self.life_span[key]
            delta[key] -= remove
            recycle = self.end_of_life[key]['recycling'] * remove
            delta['land_fill'] += self.end_of_life[key]['land_fill'] * remove
            for k, v in self.recycle[key].items():
                delta[k] += v * recycle
        for key in ['land_fill', 'mile_site_dump']:
            delta[key] -= self.products[key] * self.factor / self.life_span[key]

        for key, value in delta.items():
            self.products[key] += value

    @property
    def carbon(self):
        return sum(self.products.values())


class Products:
    def __init__(self, allocation: dict, losses: dict, end_products_kargs: dict):
        self.allocation = allocation
        self.losses = losses
        self.end_products = EndProducts(**end_products_kargs)

    def __call__(self, logwood: float, pulpwood: float, firewood: float):
        commodities = self.product_line(logwood, pulpwood)
        firewood += commodities.pop('firewood')
        self.end_products(commodities)

    def product_line(self, logwood: float, pulpwood: float):
        commodities = {
            'sawnwood': 0,
            'boards': 0,
            'paper': 0,
            'mile_site_dump': 0,
            'firewood': 0
        }

        for key, value in self.allocation['logwood'].items():
            commodities[key] = value * logwood
        for key, value in self.allocation['pulpwood'].items():
            commodities[key] = value * pulpwood

        delta = {
            'sawnwood': 0,
            'boards': 0,
            'paper': 0,
            'mile_site_dump': 0,
            'firewood': 0
        }
        for key, value in commodities.items():
            if key != 'mile_site_dump':
                decrease = sum(self.losses[key].values()) * value
                delta[key] -= decrease
                for k, v in self.losses[key].items():
                    delta[k] += v * decrease

        for key, value in delta.items():
            commodities[key] += value

        return commodities

    @property
    def carbon(self):
        return self.end_products.carbon


if __name__ == '__main__':
    pro = Products(**config.PRODUCTS_CONFIG)
    years, carbon = list(range(500)), list()

    for i in years:
        carbon.append(pro.carbon)
        pro(10, 10, 10)
    plt.plot(years, carbon)
    plt.show()
