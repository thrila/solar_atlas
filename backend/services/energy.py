import math


class Energy:
    def __init__(self, panel_output, duration_of_sunshine) -> None:
        self.panel_output = panel_output
        self.duration_of_sunshine = duration_of_sunshine

    def number_of_panels(self, expected_output):
        return math.ceil(
            expected_output / (self.panel_output * self.duration_of_sunshine)
        )

    def amount_of_power(self, panel_number):
        return panel_number * (self.panel_output * self.duration_of_sunshine)

    def emission_factor_kg(self, emission_factor_g):
        return emission_factor_g / 1000

    def equavalent_of_trees(self, emission_factor_k):
        """We are assuming that the tree is 22kg"""
        return emission_factor_k / 0.22

    def power_per_year(self, sunshine_hours):
        return self.panel_output * sunshine_hours * 365

    # def approx_setup_cost():
