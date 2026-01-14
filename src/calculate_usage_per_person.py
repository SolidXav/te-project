from avast import Avast

class Usage():
    def __init__(self, readings, device_list, household_list):
        self.room_to_person = {person.get("room"): person.get("person_id") for person in household_list if person.get("room") is not None}
        self.device_to_room = {device.get("device_id"): device["room"] for device in device_list if device.get("room") is not None}
        self.readings = readings
        self.device_list = device_list
    def calculate_usage_mapped_to_device(self):
        usage_per_device = {}
        for i in self.readings:
            dev_id = i.get("device_id")
            kwh = i.get("kwh")
            if dev_id and Avast.scan_for_cost(kwh):
                if dev_id not in usage_per_device:
                    usage_per_device[dev_id] = 0.0
                usage_per_device[dev_id] += kwh
        return usage_per_device
    def map_to_rooms(self, usage_per_device = None):
        if usage_per_device is None:
            usage_per_device = self.calculate_usage_mapped_to_device()
        usage_per_room = {}
        for i in usage_per_device:
            room = self.device_to_room.get(i, "Unknown")
            usage_per_room[room] = usage_per_room.get(room, 0) + usage_per_device[i]
        return usage_per_room
    def map_to_persons(self, usage_per_room = None):
        if usage_per_room is None:
            usage_per_room = self.map_to_rooms()
        usage_per_person = {}
        for i in usage_per_room:
            person_id = self.room_to_person.get(i, "Everyone")
            usage_per_person[person_id] = usage_per_person.get(person_id, 0) + usage_per_room[i]
        return usage_per_person
    def map_kwh_to_day(self, reading):
        dates = {}
        for i in reading:
            day = i["datetime"][:10]
            if day not in dates:
                dates[day] = 0
            if  Avast.scan_for_cost(i["kwh"]):
                dates[day] += i["kwh"]
        return dates

    def connect_everything(self, reading_list):
            return self.map_to_persons(self.map_to_rooms(self.calculate_usage_mapped_to_device()))
