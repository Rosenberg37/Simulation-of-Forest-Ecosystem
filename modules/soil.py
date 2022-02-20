from matplotlib import pyplot as plt

import config


class Soil:
    def __init__(
            self,
            initial_carbons: dict,
            invasion_rates: dict,
            decomposition_rates: dict,
            subsequent_rates: dict,
            concentration_rates: dict
    ):
        self.__dict__.update(initial_carbons)
        self.__dict__.update(invasion_rates)
        self.__dict__.update(decomposition_rates)
        self.__dict__.update(subsequent_rates)
        self.__dict__.update(concentration_rates)

    def __call__(self, foliage: float, fine_roots: float, branches: float, coarse_roots: float, stems: float):
        u_nwl = foliage + fine_roots
        u_fwl = branches + coarse_roots
        u_cwl = stems

        delta_x_nwl = u_nwl - self.a_nwl * self.x_nwl
        delta_x_fwl = u_fwl - self.a_fwl * self.x_fwl
        delta_x_cwl = u_cwl - self.a_cwl * self.x_cwl

        delta_x_ext = self.c_nwl_ext * self.a_nwl * self.x_nwl + \
                      self.c_fwl_ext * self.a_fwl * self.x_fwl + \
                      self.c_cwl_ext * self.a_cwl * self.x_cwl - self.k_ext * self.x_ext
        delta_x_cel = self.c_nwl_cel * self.a_nwl * self.x_nwl + \
                      self.c_fwl_cel * self.a_fwl * self.x_fwl + \
                      self.c_cwl_cel * self.a_cwl * self.x_cwl - self.k_cel * self.x_cel
        delta_x_lig = self.c_nwl_lig * self.a_nwl * self.x_nwl + \
                      self.c_fwl_lig * self.a_fwl * self.x_fwl + \
                      self.c_cwl_lig * self.a_cwl * self.x_cwl + \
                      self.p_ext * self.k_ext * self.x_ext + \
                      self.p_cel * self.k_cel * self.x_cel - \
                      self.k_lig * self.x_lig
        delta_x_hum1 = self.p_lig * self.k_lig * self.x_lig - self.k_hum1 * self.x_hum1
        delta_x_hum2 = self.p_hum1 * self.k_hum1 * self.x_hum1 - self.k_hum2 * self.x_hum2

        self.x_nwl += delta_x_nwl
        self.x_fwl += delta_x_fwl
        self.x_cwl += delta_x_cwl
        self.x_ext += delta_x_ext
        self.x_cel += delta_x_cel
        self.x_lig += delta_x_lig
        self.x_hum1 += delta_x_hum1
        self.x_hum2 += delta_x_hum2

    @property
    def carbon(self):
        return self.x_nwl + self.x_fwl + self.x_cwl + self.x_ext + self.x_cel + self.x_lig + self.x_hum1 + self.x_hum2


if __name__ == '__main__':
    module = Soil(**config.SOIL_OPTIONS)
    years, biomass = list(range(100)), list()
    for i in years:
        biomass.append(module.carbon)
        print(f"Year:{i},"
              f"Carbon:{module.carbon}")
        module(0, 0, 0, 0, 0)
    plt.plot(years, biomass)
    plt.show()
