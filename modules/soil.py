from matplotlib import pyplot as plt

import config


class CohortSoil:
    def __init__(self, initial_carbons: dict, concentration_rates: dict):
        self.__dict__.update(initial_carbons)
        self.__dict__.update(concentration_rates)

    @property
    def carbon(self):
        return self.x_nwl + self.x_fwl + self.x_cwl + self.x_ext + self.x_cel + self.x_lig + self.x_hum1 + self.x_hum2


class Soil:
    def __init__(
            self,
            invasion_rates: dict,
            decomposition_rates: dict,
            subsequent_rates: dict,
            cohorts_kargs: dict,
    ):
        self.__dict__.update(invasion_rates)
        self.__dict__.update(decomposition_rates)
        self.__dict__.update(subsequent_rates)

        self.cohorts = dict()
        for name, kargs in cohorts_kargs.items():
            self.cohorts[name] = CohortSoil(**kargs)

    def __call__(self, turnovers: dict):
        for name, cohort in self.cohorts.items():
            self.update(cohort, **turnovers[name])

    def update(self, cohort: CohortSoil, foliage: float, fine_roots: float, branches: float, coarse_roots: float, stems: float):
        u_nwl = foliage + fine_roots
        u_fwl = branches + coarse_roots
        u_cwl = stems
        delta_x_nwl = u_nwl - self.a_nwl * cohort.x_nwl
        delta_x_fwl = u_fwl - self.a_fwl * cohort.x_fwl
        delta_x_cwl = u_cwl - self.a_cwl * cohort.x_cwl

        delta_x_ext = cohort.c_nwl_ext * self.a_nwl * cohort.x_nwl + \
                      cohort.c_fwl_ext * self.a_fwl * cohort.x_fwl + \
                      cohort.c_cwl_ext * self.a_cwl * cohort.x_cwl - self.k_ext * cohort.x_ext
        delta_x_cel = cohort.c_nwl_cel * self.a_nwl * cohort.x_nwl + \
                      cohort.c_fwl_cel * self.a_fwl * cohort.x_fwl + \
                      cohort.c_cwl_cel * self.a_cwl * cohort.x_cwl - self.k_cel * cohort.x_cel
        delta_x_lig = cohort.c_nwl_lig * self.a_nwl * cohort.x_nwl + \
                      cohort.c_fwl_lig * self.a_fwl * cohort.x_fwl + \
                      cohort.c_cwl_lig * self.a_cwl * cohort.x_cwl + \
                      self.p_ext * self.k_ext * cohort.x_ext + \
                      self.p_cel * self.k_cel * cohort.x_cel - \
                      self.k_lig * cohort.x_lig
        delta_x_hum1 = self.p_lig * self.k_lig * cohort.x_lig - self.k_hum1 * cohort.x_hum1
        delta_x_hum2 = self.p_hum1 * self.k_hum1 * cohort.x_hum1 - self.k_hum2 * cohort.x_hum2

        cohort.x_nwl += delta_x_nwl
        cohort.x_fwl += delta_x_fwl
        cohort.x_cwl += delta_x_cwl
        cohort.x_ext += delta_x_ext
        cohort.x_cel += delta_x_cel
        cohort.x_lig += delta_x_lig
        cohort.x_hum1 += delta_x_hum1
        cohort.x_hum2 += delta_x_hum2

    @property
    def carbon(self):
        return sum(map(lambda a: a.carbon, self.cohorts.values()))


if __name__ == '__main__':
    module = Soil(**config.SOIL_CONFIG)
    years, biomass = list(range(10000)), list()
    for i in years:
        biomass.append(module.carbon)
        print(f"Year:{i},"
              f"Carbon:{module.carbon}")
        module()
    plt.plot(years, biomass)
    plt.show()
