from avast import Avast

class EfficiencyChecker:
    limit = 100
    @staticmethod
    def calculate_efficiency(rated_power_w, avg_power_w):
        return (avg_power_w / rated_power_w) * 100
    @classmethod
    def find_status_of_device(cls, efficiency):
        if efficiency > cls.limit:
            return "damaged"
        return "healthy"
    @classmethod

    def find_status_of_device_in_readings(cls, readings, devices):
        devices_list = {}
        results = {}
        for device in devices:
            if Avast.check_anomaly_for_device(device) is None:
                device_id = device.get("device_id")
                devices_list[device_id] = {
                    "name": device.get("name"),
                    "rated_power_w": device.get("rated_power_w"),
                    "readings" : []
                }
        for reading in readings:
            if Avast.check_anomaly_for_efficiency(reading, devices_list) is None:
                device_id = reading.get("device_id")
                avg_power_w = reading.get("avg_power_w")
                devices_list[device_id]["readings"].append(avg_power_w)
        for device_id, z in devices_list.items():
            rated_power_w = z["rated_power_w"]
            readings_list = z["readings"]

            if readings_list:
                avg_power_w = sum(readings_list) / len(readings_list)
                efficiency = cls.calculate_efficiency(rated_power_w, avg_power_w)
                status = EfficiencyChecker.find_status_of_device(efficiency)

                results[device_id] = {
                    "name" : z.get("name"),
                    "rated_power_w" : z.get("rated_power_w"),
                    "avg_power_w" : round(z.get("avg_power_w"), 2),
                    "efficiency" : round(efficiency, 2),
                    "status" : status
                    "is_damaged": efficiency > cls.limit
                    "readings": len(readings_list)

                }

        return results

    @classmethod
    def get_damaged(cls, readings, devices):
        all_results = cls.find_status_of_device_in_readings(readings, devices)
        return {device_id: z for device_id, z in all_results.items() if z["is_damaged"]}

    @classmethod
    def get_healthy(cls, readings, devices):
        all_results = cls.find_status_of_device_in_readings(readings, devices)
        return {device_id: z for device_id, z in all_results.items() if not z["is_damaged"]}

    @classmethod
    def report(cls, readings, devices):
        results = cls.find_status_of_device_in_readings(readings, devices)
        damaged = []
        healthy = []

        for device_id, z in results.items():
            if z["healthy"]:
                healthy.append(f"{z['name']} has efficiency equals {z['efficiency']}%, Device is {z['status'].upper()}")
            else:
                damaged.append(f"{z['name']} has efficiency equals {z['efficiency']}%, Device is {z['status'].upper()}")

        if healthy:
            print(f"Healthy devices: ")
            for pomidor in healthy:
                print(f"{pomidor}")
        if damaged:
            print(f"Damaged devices: ")
            for pomidor in damaged:
                print(f"{pomidor}")

        print(f"Total of healthy devices: {len(healthy)}, Total of damaged devices: {len(damaged)}")

