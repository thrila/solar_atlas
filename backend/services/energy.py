import math


class Energy:
    def __init__(self, panel_output, duration_of_sunshine) -> None:
        self.panel_output = panel_output
        self.duration_of_sunshine = duration_of_sunshine

    def number_of_panels(self, expected_output):
        """amount of panels required to generate expected output (in watts) per day"""
        return math.ceil(
            expected_output / (self.panel_output * self.duration_of_sunshine)
        )

    def amount_of_power(self, panel_number=1):
        """Enter amount of panels you have. we will cap their output at 330w"""
        return panel_number * (self.panel_output * self.duration_of_sunshine)

    def kWh_per_household(self, kWh_per_person, avg_household_size):
        return float(kWh_per_person) * float(avg_household_size)

    def national_energy_demand(self, kWh_per_person, population):
        return float(kWh_per_person) * float(population)

    def co2_saving_potential(self, kWh_per_person, carbon_intensity):
        return (float(kWh_per_person) * float(carbon_intensity)) / 1000

    def auto_suggest(self):
        """This should autosuggest solar for places"""
