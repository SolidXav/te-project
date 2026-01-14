class Avast:
# Avast wyłapuje anomalie None, czeski film - nikt nic nie wie oraz wartości niedodatnie, bo żadne urządzenie nie oddaje energii (jak np windy, silniki)
    @staticmethod
    def check_anomaly_for_reading(reading, device_list):
        if reading.get("kwh") is None or reading.get("kwh") < 0:
            return "invalid kwh"
        if reading.get("device_id") is None or reading.get("device_id") not in device_list:
            return "Device not found"
        if reading.get("avg_power_w") is None or reading.get("avg_power_w") < 0:
            return "invalid avg_power_w"
        if reading.get("datetime") is None:
            return "No datetime"
        return None
    @staticmethod
    def check_anomaly_for_device(device):
        if device is None:
            return "Device not found"
        if device.get("room") is None:
            return "No room"
        if device.get("rated_power_w") is None or device.get("rated_power_w")  <= 0:
            return "invalid power"
        return None
    @staticmethod
    def check_anomaly_for_event(event, device_list):
        if event.get("device_id") is None or event.get("device_id") not in device_list:
            return "Device not found"
        return None
    @staticmethod
    def scan_for_cost(value):
        if value is None or value < 0:
            return False
        return True
    @staticmethod
    def correct_day(reading):
        date = reading.get("datetime")
        if date and isinstance(date, str) and len(date) >= 10:
            return date[:10]
        return None
    @staticmethod
    def check_anomaly_for_efficiency(reading, device_list):
        device_id = reading.get("device_id")
        avg_power_w = reading.get("avg_power_w")
        if device_id is None or device_id not in device_list:
            return "Device not found"
        if avg_power_w is None or avg_power_w < 0:
            return "invalid avg_power_w"
        rated_power_w = device_list.get(device_id)
        if rated_power_w is None or rated_power_w <= 0:
            return "invalid rated_power_w"
        return None
    def __str__(self):
        return "Baza wirusów programu Avast została zaktualizowana"
