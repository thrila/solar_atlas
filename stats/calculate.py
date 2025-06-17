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


if __name__ == "__main__":
    elec = Energy(350, 8.3)
    print(elec.amount_of_power(16))
    print("-------")
    print(elec.number_of_panels(20000))
