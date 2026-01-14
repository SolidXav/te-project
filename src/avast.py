class Avast:
# Avast wyłapuje anomalie None, czeski film - nikt nic nie wie oraz wartości niedodatnie, bo żadne urządzenie nie oddaje energii (jak np windy, silniki)
    @staticmethod
    def scan(reading, device_to_room):
        if reading.kwh is None or reading.device_id is None or reading.device_id not in device_to_room:
            return False
        return True
    @staticmethod
    def scan_for_percentage(reading, device):
        if device is None or device.rated_power_w is None or device.rated_power_w == 0:
            return False
        return True
    @staticmethod
    def scan_for_cost(value):
        if value is None or value < 0:
            return False
        return True
    @staticmethod
    def scan_day(day):
        if day is not None and isinstance(day, str):
            return True
        return False