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

    def per_person(self, map_to_persons, household_count=3):
        person_costs = {}
        everyone_kwh = map_to_persons.get("Everyone", 0)
        everyone_cost_per_person = 0

        if Avast.scan_for_cost(everyone_kwh) and household_count > 0:
            everyone_cost_per_person = round((everyone_kwh * self.price_per_kwh) / household_count, 2)

        for person_id, kwh in map_to_persons.items():
            if person_id == "Everyone":
                continue

            if Avast.scan_for_cost(kwh):
                personal_cost = round(kwh * self.price_per_kwh, 2)
                person_costs[person_id] = round(personal_cost + everyone_cost_per_person, 2)

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

    def per_event(self, events, readings):
        event_costs = []

        i = 0
        while i < len(events):
            if i + 1 >= len(events):
                break
            start_event = events[i]
            stop_event = events[i + 1]
            if not Avast.check_event_pair(start_event, stop_event):
                i += 1
                continue

            device_id = start_event["device_id"]
            start_date = start_event["date"]
            stop_date = stop_event["date"]
            cycle_kwh = 0
            for reading in readings:
                if reading.get("device_id") != device_id:
                    continue

                reading_date = reading.get("datetime", "")[:10]
                if reading_date >= start_date and reading_date <= stop_date:
                    kwh_value = reading.get("kwh", 0)
                    if Avast.scan_for_cost(kwh_value):
                        cycle_kwh += kwh_value
            cycle_cost = round(cycle_kwh * self.price_per_kwh, 2)
            mode = start_event.get("details", {}).get("mode") or \
                   start_event.get("details", {}).get("program") or \
                   "cykl"
            event_name = f"{device_id} ({mode})"

            event_costs.append({
                "event_id": start_event["event_id"],
                "device_id": device_id,
                "name": event_name,
                "start_date": start_date,
                "stop_date": stop_date,
                "kwh": round(cycle_kwh, 2),
                "cost": cycle_cost
            })
            i += 2
        return event_costs