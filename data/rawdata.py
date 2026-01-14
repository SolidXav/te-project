DATASET = {
    "meta": {
        "dataset_id": "smart_home_energy_v1",
        "energy_unit": "kWh",
        "power_unit": "W",
        "notes": [
            "Dane dotyczą inteligentnego domu: urządzenia, odczyty energii i zdarzenia.",
            "Każdy odczyt to zużycie w danej godzinie (kWh) oraz średnia moc (W).",
            "Występują braki: missing device_id, missing kwh.",
            "Występują anomalie: ujemne kWh, ekstremalnie wysoka moc, odczyt dla nieznanego urządzenia."
        ]
    },

    # Domownicy (opcjonalnie do analiz kto generuje zużycie)
    "household": [
        {"person_id": "H001", "role": "adult", "room": "living"},
        {"person_id": "H002", "role": "adult", "room": "office"},
        {"person_id": "H003", "role": "child", "room": "bedroom"},
    ],

    # Urządzenia w domu – rated_power_w do weryfikacji anomalii
    "devices": [
        {"device_id": "D001", "name": "HeatPump", "type": "hvac", "room": "utility", "rated_power_w": 2500},
        {"device_id": "D002", "name": "Oven", "type": "kitchen", "room": "kitchen", "rated_power_w": 3000},
        {"device_id": "D003", "name": "PC", "type": "electronics", "room": "office", "rated_power_w": 650},
        {"device_id": "D004", "name": "Fridge", "type": "kitchen", "room": "kitchen", "rated_power_w": 180},
        {"device_id": "D005", "name": "Washer", "type": "laundry", "room": "utility", "rated_power_w": 2200},
        {"device_id": "D006", "name": "Lights", "type": "lighting", "room": "living", "rated_power_w": 120},
        {"device_id": "D999", "name": "TestDevice", "type": "unknown", "room": None, "rated_power_w": 0},
    ],

    # Zdarzenia (np. uruchomienie prania, pieczenia) – mogą korelować z poborem
    "events": [
        {"event_id": 14001, "date": "2025-02-10", "time": "18:10", "device_id": "D002", "event": "start",
         "details": {"mode": "bake", "temp_c": 200}},
        {"event_id": 14002, "date": "2025-02-10", "time": "19:05", "device_id": "D002", "event": "stop", "details": {}},
        {"event_id": 14003, "date": "2025-02-11", "time": "07:15", "device_id": "D005", "event": "start",
         "details": {"program": "cotton"}},
        {"event_id": 14004, "date": "2025-02-11", "time": "08:30", "device_id": "D005", "event": "stop", "details": {}},
        {"event_id": 14005, "date": "2025-02-12", "time": "20:00", "device_id": "D404", "event": "start",
         "details": {}},
    ],

    # Odczyty godzinowe – każdy rekord to jedna godzina dla jednego urządzenia
    "readings": [
        {"reading_id": 15001, "datetime": "2025-02-10 18:00", "device_id": "D002", "kwh": 1.20, "avg_power_w": 2500},
        {"reading_id": 15002, "datetime": "2025-02-10 19:00", "device_id": "D002", "kwh": 0.60, "avg_power_w": 1800},
        {"reading_id": 15003, "datetime": "2025-02-10 18:00", "device_id": "D004", "kwh": 0.05, "avg_power_w": 120},
        {"reading_id": 15004, "datetime": "2025-02-10 19:00", "device_id": "D004", "kwh": 0.06, "avg_power_w": 140},
        {"reading_id": 15005, "datetime": "2025-02-10 18:00", "device_id": "D006", "kwh": 0.02, "avg_power_w": 90},
        {"reading_id": 15006, "datetime": "2025-02-10 19:00", "device_id": "D006", "kwh": 0.03, "avg_power_w": 110},

        {"reading_id": 15007, "datetime": "2025-02-11 07:00", "device_id": "D005", "kwh": 0.80, "avg_power_w": 2100},
        {"reading_id": 15008, "datetime": "2025-02-11 08:00", "device_id": "D005", "kwh": 0.70, "avg_power_w": 2000},
        {"reading_id": 15009, "datetime": "2025-02-11 07:00", "device_id": "D003", "kwh": 0.10, "avg_power_w": 120},
        {"reading_id": 15010, "datetime": "2025-02-11 08:00", "device_id": "D003", "kwh": 0.18, "avg_power_w": 220},

        {"reading_id": 15011, "datetime": "2025-02-12 06:00", "device_id": "D001", "kwh": 2.80, "avg_power_w": 3200},
        {"reading_id": 15012, "datetime": "2025-02-12 07:00", "device_id": "D001", "kwh": 2.60, "avg_power_w": 2900},
        {"reading_id": 15013, "datetime": "2025-02-12 20:00", "device_id": "D002", "kwh": -0.40, "avg_power_w": 1500},
        {"reading_id": 15014, "datetime": "2025-02-12 21:00", "device_id": None, "kwh": 0.10, "avg_power_w": 100},
        {"reading_id": 15015, "datetime": "2025-02-12 22:00", "device_id": "D404", "kwh": 0.50, "avg_power_w": 500},

        {"reading_id": 15016, "datetime": "2025-02-13 18:00", "device_id": "D004", "kwh": None, "avg_power_w": 130},
        {"reading_id": 15017, "datetime": "2025-02-13 18:00", "device_id": "D006", "kwh": 0.04, "avg_power_w": 160},
        {"reading_id": 15018, "datetime": "2025-02-13 19:00", "device_id": "D006", "kwh": 0.05, "avg_power_w": 5000},
    ]
}
