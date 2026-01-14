class Meta:
    def __init__(self, dataset_id, energy_unit, power_unit):
        self.dataset_id = dataset_id
        self.energy_unit = energy_unit
        self.power_unit = power_unit
    @classmethod
    def from_dict(cls, data):
        return cls(
            dataset_id=data['dataset_id'],
            energy_unit=data['energy_unit'],
            power_unit=data['power_unit']
        )
class Household:
    def __init__(self, person_id, role, room):
        self.person_id = person_id
        self.role = role
        self.room = room
    @classmethod
    def from_dict(cls, data):
        return cls(
            person_id=data['person_id'],
            role=data['role'],
            room=data['room']
        )
class Device:
    def __init__(self, device_id, name, type, room, rated_power_w):
        self.device_id = device_id
        self.name = name
        self.type = type
        self.room = room
        self.rated_power_w = rated_power_w
    @classmethod
    def from_dict(cls, data):
        return cls(
            device_id=data['device_id'],
            name=data['name'],
            type=data['type'],
            room=data['room'],
            rated_power_w=data['rated_power_w']
        )
class Event:
    def __init__(self, event_id, date, time, device_id, event, details):
        self.event_id = event_id
        self.date = date
        self.time = time
        self.device_id = device_id
        self.event = event
        self.details = details
    @classmethod
    def from_dict(cls, data):
        return cls(
            event_id=data['event_id'],
            date=data['date'],
            time=data['time'],
            device_id=data['device_id'],
            event=data['event'],
            details=data['details']
        )

class Reading:
    def __init__(self, reading_id, date_time, device_id, kwh, avg_power_w):
        self.reading_id = reading_id
        self.date_time = date_time
        self.device_id = device_id
        self.kwh = kwh
        self.avg_power_w = avg_power_w
    @classmethod
    def from_dict(cls, data):
        return cls(
            reading_id=data['reading_id'],
            date_time=data['datetime'],
            device_id=data['device_id'],
            kwh=data['kwh'],
            avg_power_w=data['avg_power_w']
        )
