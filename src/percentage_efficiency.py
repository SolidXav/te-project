class EfficiencyChecker:
    @staticmethod
    def calculate_efficiency(rated_power_w, avg_power_w):
        try:
            eff = avg_power_w / rated_power_w
            return eff*100
        except ZeroDivisionError:
            return 0.00