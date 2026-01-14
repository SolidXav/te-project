from avast import Avast

class DeviceMapper:

    def __init__(self, readings, device_to_room):
        self.readings = readings
        self.device_to_room = device_to_room

    def map(self):
        devices = set(self.device_to_room.keys())
        usage = {}
        for reading in self.readings:
            if Avast.check_anomaly_for_reading(reading, devices) is None:
                deviceid = reading.get("device_id")
                usage[deviceid] = usage.get(deviceid, 0.0) + reading.get("kwh", 0.0)
        return usage

class RoomMapper:

    def __init__(self, device_to_room):
        self.device_to_room = device_to_room

    def map(self, usage_per_device):
        usage = {}
        for device_id, kwh in usage_per_device.items():
            room = self.device_to_room.get(device_id, "Unknown")
            usage[room] = usage.get(room, 0.0) + kwh
        return usage

class PersonMapper:

    def __init__(self, room_to_person):
        self.room_to_person = room_to_person

    def map(self, usage_per_room):
        usage = {}
        for room, kwh in usage_per_room.items():
            person = self.room_to_person.get(room, "Everyone")
            usage[person] = usage.get(person, 0.0) + kwh
        return usage

class DayMapper:

    def __init__(self, readings, device_to_room):
        self.readings = readings
        self.device_to_room = device_to_room

    def map(self):
        devices = set(self.device_to_room.keys())
        dates = {}
        for reading in self.readings:
            if Avast.check_anomaly_for_reading(reading, devices) is None:
                day = Avast.correct_day(reading)
                if day:
                    kwh = reading.get("kwh", 0.0)
                    dates[day] = dates.get(day, 0) + kwh
        return dates

class Usage:

    def __init__(self, readings, device_list, household_list):
        self.room_to_person = {person.get("room"): person.get("person_id") for person in household_list if person.get("room") is not None}
        self.device_to_room = {device.get("device_id"): device["room"] for device in device_list if device.get("room") is not None}
        self.readings = readings

    def get_usage_per_device(self):
        mapper = DeviceMapper(self.readings, self.device_to_room)
        return mapper.map()

    def get_usage_per_room(self):
        usage_per_device = self.get_usage_per_device()
        mapper = RoomMapper(self.device_to_room)
        return mapper.map(usage_per_device)

    def get_usage_per_household(self):
        usage_per_room = self.get_usage_per_room()
        mapper = PersonMapper(self.room_to_person)
        return mapper.map(usage_per_room)

    def get_usage_per_day(self):
        return DayMapper(self.readings, self.device_to_room).map()

    def start(self):
        return {
            "usage_per_device": self.get_usage_per_device(),
            "usage_per_room": self.get_usage_per_room(),
            "usage_per_household": self.get_usage_per_household(),
            "usage_per_day": self.get_usage_per_day(),
        }
# mike oxlong fr
## Avasta otrzymuje tylko devicemapper oraz daymapper, ponieważ działają na surowych danych. Reszta dostaje przefiltrowane