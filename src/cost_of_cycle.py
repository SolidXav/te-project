from avast import Avast

class Calculator:
    def __init__(self, price_per_kwh=0.89):
        self.price_per_kwh = price_per_kwh
    def per_device(self, usage_per_device):
        device_costs = {}
        for device_id, kwh in usage_per_device.items():
            if Avast.scan_for_cost(kwh):
                device_costs[device_id] = round(kwh * self.price_per_kwh, 2)
        return device_costs
    def per_person(self, map_to_persons):
        person_costs = {}
        for person_id, kwh in map_to_persons.items():
            if Avast.scan_for_cost(kwh):
                person_costs[person_id] = round(kwh * self.price_per_kwh, 2)
        return person_costs

    def per_room(self, map_to_rooms):
        room_costs = {}
        for room, kwh in map_to_rooms.items():
            if Avast.scan_for_cost(kwh):
                room_costs[room] = round(kwh * self.price_per_kwh, 2)
        return room_costs

    def per_day(self, map_kwh_to_day):
        day_costs = {}
        for day, kwh in map_kwh_to_day.items():
            if Avast.scan_for_cost(kwh):
                day_costs[day] = round(kwh * self.price_per_kwh, 2)
        return day_costs