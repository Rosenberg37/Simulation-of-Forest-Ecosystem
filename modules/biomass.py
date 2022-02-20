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
            the turnover stem biomass of this year
        """
        growth = self.trans2biomass(utils.polygonal(self.CAIs, age))
        self.biomass += growth

        nature_rate = utils.polygonal(self.mortality, age)
        manage_rate = sum(map(lambda a: a(), self.impacts))
        self.impacts = list(filter(lambda a: a.not_done, self.impacts))
        turnover = (nature_rate + manage_rate) * self.biomass
        self.biomass -= turnover

        return growth, turnover

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
        :return: the turnover amount to soil module.
R       """
        self.biomass += growth_stem * utils.polygonal(self.relative_growth, age)
        turnover = self.turnover_rate * self.biomass
        self.biomass -= turnover
        return turnover

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
                'stem': {
                    'LogWood': thinning_harvest_dict['stem']['LogWood'][i],
                    'PulpPap': thinning_harvest_dict['stem']['PulpPap'][i],
                    'Slash': thinning_harvest_dict['stem']['Slash'][i],
                },
                'branches': {
                    'LogWood': thinning_harvest_dict['branches']['LogWood'][i],
                    'PulpPap': thinning_harvest_dict['branches']['PulpPap'][i],
                    'Slash': thinning_harvest_dict['branches']['Slash'][i],
                },
            })

        self.stem = Stem(**stem_kargs)
        self.compartments = compartments_kargs
        for name, kargs in self.compartments.items():
            self.compartments[name] = Compartment(**kargs)

    def __call__(self) -> tuple[dict, dict]:
        growth, stem_turnover = self.stem(self.age)
        turnovers = {
            'foliage': None,
            'branches': None,
            'roots': None
        }
        for name, com in self.compartments.items():
            turnovers[name] = com(growth, self.age)
        self.age += 1

        material = {
            'LogWood': 0,
            'PulpPap': 0,
            'Slash': 0
        }
        for i, harvest in enumerate(self.thinning_harvest):
            if harvest['age'] == self.age:
                fraction = harvest['fraction']
                total_remove = 0

                for com, com_h in zip([self.stem, self.compartments['branches']], [harvest['stem'], harvest['branches']]):
                    remove = com.biomass * fraction
                    total_remove += remove
                    com.biomass -= remove

                    material['LogWood'] += remove * com_h['LogWood']
                    material['PulpPap'] += remove * com_h['PulpPap']
                    material['Slash'] += remove * com_h['Slash']
                remove = self.compartments['foliage'].biomass * fraction
                material['Slash'] += self.compartments['foliage'].biomass
                self.compartments['foliage'].biomass -= remove
                total_remove += remove

                remove = self.compartments['roots'].biomass * fraction
                self.compartments['roots'].biomass -= remove
                total_remove += self.compartments['roots'].biomass * fraction

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
        return self.stem.biomass + sum(map(lambda a: a.biomass, self.compartments.values()))


class Biomass:
    def __init__(self, cohorts_kargs: list[dict]):
        self.cohorts = [Cohort(**kargs) for kargs in cohorts_kargs]

    def __call__(self):
        turnovers, materials = zip(*[coh() for coh in self.cohorts])

        material = {
            'LogWood': sum(map(lambda a: a['LogWood'], materials)),
            'PulpPap': sum(map(lambda a: a['PulpPap'], materials)),
            'Slash': sum(map(lambda a: a['Slash'], materials))
        }

        return material

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.cohorts))

    @property
    def biomass(self):
        return sum(map(lambda a: a.biomass, self.cohorts))


if __name__ == '__main__':
    module = Biomass(config.BIOMASS_OPTIONS)
    years, biomass = list(range(200)), list()
    for i in years:
        biomass.append(module.biomass)
        print(f"Year:{i},"
              f"Carbon:{module.carbon},"
              f"Biomass:{module.biomass} ")
        module()
    plt.plot(years, biomass)
    plt.show()
