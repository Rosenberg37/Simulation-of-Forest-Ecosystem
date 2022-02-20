from enum import Enum

from matplotlib import pyplot as plt

import config
import utils


class Impact:
    def __init__(self, management_mortality: list[tuple], volume: float):
        self.single = len(management_mortality) == 1
        if self.single:
            _, self.start_mort, self.impact_time = management_mortality[0]
            self.t = self.impact_time + 1
        else:
            mortality = sorted(management_mortality, key=lambda a: a[0])
            for m in mortality:
                if m[0] <= volume:  # find the lower bound
                    v1, self.start_mort1, self.impact_time1 = m
            for m in reversed(mortality):
                if m[0] >= volume:  # find the upper bound
                    v2, self.start_mort2, self.impact_time2 = m
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
            initial_carbon: float = 0,
    ):
        self.mortality = list(zip(*mortality_dict.values()))
        self.CAIs = list(zip(*CAI_dict.values()))
        self.wood_density = wood_density
        self.carbon_content = carbon_content

        self.biomass = initial_carbon / self.carbon_content
        self.impacts = list()

    def __call__(self, age: int):
        """

        :param age: this age of the cohort
        :return:
            the growth biomass of this year.
            the turnover carbon amount of this year
        """
        growth = self.trans2biomass(utils.polygonal(self.CAIs, age))
        self.biomass += growth

        nature_rate = utils.polygonal(self.mortality, age)
        manage_rate = sum(map(lambda a: a(), self.impacts))
        self.impacts = list(filter(lambda a: a.not_done, self.impacts))
        turnover = (nature_rate + manage_rate) * self.biomass
        self.biomass -= turnover

        return growth, turnover * self.carbon_content

    @property
    def carbon(self):
        return self.biomass * self.carbon_content

    def trans2volume(self, biomass):
        return biomass / self.wood_density

    def trans2biomass(self, volume):
        return volume * self.wood_density


class Compartment:
    def __init__(
            self,
            carbon_content: float,
            turnover_rate: float,
            relative_growth_dict: dict,
            initial_carbon: float = 0,
    ):
        self.initial_carbon = initial_carbon
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
    class CohortType(Enum):
        # This latter information is used to characterise the quality of the litter input to the soil module.
        coniferous = 0
        broadleaved = 1

    # growth function defined by age.
    def __init__(
            self,
            cohort_type: CohortType,
            thinning_harvest_dict: dict,
            stem_kargs: dict,
            compartments_kargs: dict,
            management_mortality_dict: dict,
            competition: list[tuple] = None,
            initial_age: int = 0,
    ):
        self.age = initial_age
        self.cohort_type = cohort_type
        self.competition = competition  # TODO(implement)
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
            })

        self.stem = Stem(**stem_kargs)
        self.compartments = compartments_kargs
        for name, kargs in self.compartments.items():
            self.compartments[name] = Compartment(**kargs)

    def __call__(self) -> tuple[dict, dict]:
        growth, stem_turnover = self.stem(self.age)
        turnovers = {'stems': stem_turnover}
        for name, com in self.compartments.items():
            turnovers[name] = com(growth, self.age)
        self.age += 1

        material = {
            'logwood': 0,
            'pulpwood': 0,
            'slash': 0
        }
        for i, harvest in enumerate(self.thinning_harvest):
            if harvest['age'] == self.age:
                fraction = harvest['fraction']

                for com, com_h in zip([self.stem, self.compartments['branches']], [harvest['stems'], harvest['branches']]):
                    remove = com.biomass * fraction
                    com.biomass -= remove

                    material['logwood'] += remove * com_h['logwood']
                    material['pulpwood'] += remove * com_h['pulpwood']
                    material['slash'] += remove * com_h['slash']
                remove = self.compartments['foliage'].carbon * fraction
                material['slash'] += remove
                self.compartments['foliage'].biomass -= remove
                self.compartments['roots'].biomass *= (1 - fraction)

                remove_volume = self.stem.biomass * fraction / self.stem.wood_density
                self.stem.impacts.append(Impact(self.management_mortality, remove_volume))
                if i == len(self.thinning_harvest) - 1:
                    self.age = 0

        return turnovers, material

    @property
    def carbon(self):
        return self.stem.carbon + sum(map(lambda a: a.carbon, self.compartments.values()))

    @property
    def biomass(self):
        return self.stem.biomass + sum(map(lambda a: a.carbon, self.compartments.values()))


class Biomass:
    def __init__(self, cohorts_kargs: list[dict]):
        self.cohorts = [Cohort(**kargs) for kargs in cohorts_kargs]

    def __call__(self):
        turnovers, materials = zip(*[coh() for coh in self.cohorts])

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
        return sum(map(lambda a: a.carbon, self.cohorts))

    @property
    def biomass(self):
        return sum(map(lambda a: a.carbon, self.cohorts))


if __name__ == '__main__':
    module = Biomass(config.BIOMASS_CONFIG)
    years, biomass = list(range(200)), list()
    for i in years:
        biomass.append(module.biomass)
        print(f"Year:{i},"
              f"Carbon:{module.carbon},"
              f"Biomass:{module.biomass} ")
        module()
    plt.plot(years, biomass)
    plt.show()
