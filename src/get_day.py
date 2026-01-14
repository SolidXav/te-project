from avast import Avast
class Date:
    def get_day(self, reading):
        date = reading["timestamp"]
        if Avast.scan_day(date):
            return reading["timestamp"][:10]
        return "Unknown"