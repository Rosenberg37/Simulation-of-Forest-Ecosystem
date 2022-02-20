from matplotlib import pyplot as plt

import config
from modules import utils


class Impact:
    def __init__(self, management_mortality: list[tuple], volume: float):
        self.single = len(management_mortality) == 1
        if self.single:
            _, self.start_mort, self.impact_time = management_mortality[0]
            self.t = self.impact_time + 1
        else:
            mort = sorted(management_mortality, key=lambda a: a[0])

            v1 = self.start_mort1 = self.impact_time1 = None
            v2 = self.start_mort2 = self.impact_time2 = None
            for m in mort:
                if m[0] <= volume:  # find the lower bound
                    v1, self.start_mort1, self.impact_time1 = m
            for m in reversed(mort):
                if m[0] >= volume:  # find the upper bound
                    v2, self.start_mort2, self.impact_time2 = m

            if v1 is None:
                self.single = True
                _, self.start_mort, self.impact_time = mort[0]
                self.t = self.impact_time + 1
            elif v2 is None:
                self.single = True
                _, self.start_mort, self.impact_time = mort[-1]
                self.t = self.impact_time + 1
            else:
                self.t = max(self.impact_time1, self.impact_time2) + 1
                self.factor1 = (volume - v1) / (v2 - v1)
                self.factor2 = (v2 - volume) / (v2 - v1)

    def __call__(self):
        self.t -= 1
        if self.single:
            return self.start_mort * (self.impact_time - self.t) / self.impact_time
        else:
            rate1 = max(self.start_mort1 * (self.impact_time1 - self.t) / self.impact_time1, 0)
            rate2 = max(self.start_mort2 * (self.impact_time2 - self.t) / self.impact_time2, 0)
            return rate1 * self.factor1 + rate2 * self.factor2

    @property
    def not_done(self):
        return self.t > 0


class Stem:
    def __init__(
            self,
            carbon_content: float,
            wood_density: float,
            mortality_dict: dict,
            CAI_dict: dict,  # Current annual volume increment
            initial_carbon: float,
    ):
        self.mortality = list(zip(*mortality_dict.values()))
        self.CAIs = list(zip(*CAI_dict.values()))
        self.wood_density = wood_density
        self.carbon_content = carbon_content

        self.biomass = initial_carbon / self.carbon_content
        self.impacts = list()

    def __call__(self, mg_rate: float, age: int):
        """

        :param mg_rate: decrease rate of growth because of competition
        :param age: this age of the cohort
        :return:
            the growth biomass of this year.
            the turnover carbon amount of this year
        """
        growth = utils.polygonal(self.CAIs, age) * self.wood_density * mg_rate

        nature_rate = utils.polygonal(self.mortality, age)
        manage_rate = sum(map(lambda a: a(), self.impacts))
        self.impacts = list(filter(lambda a: a.not_done, self.impacts))
        turnover = (nature_rate + manage_rate) * self.biomass

        self.biomass += growth - turnover
        return growth, turnover

    @property
    def carbon(self):
        return self.biomass * self.carbon_content


class Compartment:
    def __init__(
            self,
            carbon_content: float,
            turnover_rate: float,
            relative_growth_dict: dict,
            initial_carbon: float,
    ):
        self.carbon_content = carbon_content
        self.turnover_rate = turnover_rate
        self.relative_growth = list(zip(*relative_growth_dict.values()))

        self.biomass = initial_carbon / self.carbon_content

    def __call__(self, growth_stem: float, age: int):
        """
        grow with stem and then turnover.
        :param growth_stem: the growth of biomass of the stem this year
        :param age: this age of the cohort
        :return: the turnover carbon amount to soil module.
R       """
        self.biomass += growth_stem * utils.polygonal(self.relative_growth, age)
        turnover = self.turnover_rate * self.biomass
        self.biomass -= turnover
        return turnover * self.carbon_content

    @property
    def carbon(self):
        return self.biomass * self.carbon_content


class Cohort:
    def __init__(
            self,
            initial_age: int,
            maximum_biomass: float,
            thinning_harvest_dict: dict,
            stem_kargs: dict,
            compartments_kargs: dict,
            management_mortality_dict: dict,
    ):
        self.age = initial_age
        self.maximum_biomass = maximum_biomass
        self.management_mortality = list(zip(*management_mortality_dict.values()))

        self.thinning_harvest = list()
        for i, age in enumerate(thinning_harvest_dict['age']):
            self.thinning_harvest.append({
                'age': thinning_harvest_dict['age'][i],
                'fraction': thinning_harvest_dict['fraction'][i],
                'stems': {
                    'logwood': thinning_harvest_dict['stems']['logwood'][i],
                    'pulpwood': thinning_harvest_dict['stems']['pulpwood'][i],
                    'slash': thinning_harvest_dict['stems']['slash'][i],
                },
                'branches': {
                    'logwood': thinning_harvest_dict['branches']['logwood'][i],
                    'pulpwood': thinning_harvest_dict['branches']['pulpwood'][i],
                    'slash': thinning_harvest_dict['branches']['slash'][i],
                },
                'slash_soil': thinning_harvest_dict['slash_soil'][i],
            })

        self.compartments = {'stems': Stem(**stem_kargs)}
        for name, kargs in compartments_kargs.items():
            self.compartments[name] = Compartment(**kargs)

    def __call__(self, mg_rate: float) -> tuple[dict, dict]:
        growth, stem_turnover = self.compartments['stems'](mg_rate, self.age)
        turnovers = {'stems': stem_turnover}
        for name in ['foliage', 'branches', 'roots']:
            turnovers[name] = self.compartments[name](growth, self.age)

        material = {
            'logwood': 0,
            'pulpwood': 0,
        }
        for i, harvest in enumerate(self.thinning_harvest):
            if harvest['age'] == self.age:
                fraction = harvest['fraction']
                remove_volume = self.compartments['stems'].biomass * fraction / self.compartments['stems'].wood_density
                self.compartments['stems'].impacts.append(Impact(self.management_mortality, remove_volume))

                for name in ['stems', 'branches']:
                    remove = self.compartments[name].biomass * fraction
                    self.compartments[name].biomass -= remove

                    material['logwood'] += remove * harvest[name]['logwood']
                    material['pulpwood'] += remove * harvest[name]['pulpwood']
                    turnovers[name] += remove * harvest[name]['slash'] * harvest['slash_soil']

                for name in ['foliage', 'roots']:
                    remove = self.compartments[name].biomass * fraction
                    turnovers[name] += remove * self.compartments[name].carbon_content
                    self.compartments[name].biomass -= remove

                self.age = -1 if i == len(self.thinning_harvest) - 1 else self.age

        self.age += 1
        return turnovers, material

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.compartments.values()))

    @property
    def biomass(self):
        return sum(map(lambda a: a.carbon, self.compartments.values()))


class Biomass:
    def __init__(self, cohorts_kargs: dict):
        self.competitions, self.cohorts = dict(), dict()
        for key, kargs in cohorts_kargs.items():
            kargs = kargs.copy()
            self.competitions[key] = kargs.pop('competition')
            self.cohorts[key] = Cohort(**kargs)

    def __call__(self):
        turnovers, materials = list(), list()

        for name, cohort in self.cohorts.items():
            competition = self.competitions[name].copy()
            bio_rates = competition.pop('bio_rates')
            mg_rate = 1
            for n, c in competition.items():
                points = list(zip(bio_rates, c))
                rate = self.cohorts[n].biomass / self.cohorts[n].maximum_biomass
                mg_rate *= utils.polygonal(points, rate)
            turnover, material = cohort(mg_rate)
            turnovers.append(turnover)
            materials.append(material)

        material = dict()
        for key in materials[0].keys():
            material[key] = sum(map(lambda a: a[key], materials))

        turnover = dict()
        for key in turnovers[0].keys():
            if key == 'roots':
                turnover['fine_roots'] = 0
                turnover['coarse_roots'] = 0
                for t in turnovers:
                    root = t['roots']
                    rate = t['foliage'] / (t['branches'] + t['foliage'])
                    turnover['fine_roots'] += rate * root
                    turnover['coarse_roots'] += (1 - rate) * root
            else:
                turnover[key] = sum(map(lambda a: a[key], turnovers))

        return material, turnover

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.cohorts.values()))

    @property
    def biomass(self):
        return sum(map(lambda a: a.biomass, self.cohorts.values()))


if __name__ == '__main__':
    module = Biomass(config.BIOMASS_CONFIG)
    years, biomass = list(range(100)), list()
    for i in years:
        biomass.append(module.biomass)
        print(f"Year:{i},"
              f"Carbon:{module.carbon},"
              f"Biomass:{module.biomass} ")
        module()
    plt.plot(years, biomass)
    plt.show()
