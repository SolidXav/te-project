from calculate_usage_per_person import Usage
from cost_of_cycle import Calculator
from data.rawdata import DATASET
from avast import Avast

def main():
    # 1. INICJALIZACJA
    # Przekazujemy listy z dużego słownika DATASET
    u = Usage(DATASET["readings"], DATASET["devices"], DATASET["household"])
    calc = Calculator(price_per_kwh=0.89)

    readings = DATASET["readings"]
    events = DATASET["events"]

    print("=" * 50)
    print("SERWIS ANALITYCZNY INTELIGENTNEGO DOMU")
    print("=" * 50)

    # --- 2. PERCENTAGE EFFICIENCY ---
    total_count = len(readings)
    valid_count = sum(1 for r in readings if Avast.scan_for_cost(r["kwh"]))
    efficiency = (valid_count / total_count) * 100 if total_count > 0 else 0

    print(f"\n[SYSTEM] Wydajność danych: {efficiency:.2f}%")
    print(f"[SYSTEM] Rekordy poprawne: {valid_count} | Błędne: {total_count - valid_count}")

    # --- 3. COST PER DEVICE ---
    device_kwh = u.calculate_usage_mapped_to_device()
    device_costs = calc.per_device(device_kwh)

    print(f"\n{'URZĄDZENIE':<15} | {'KOSZT (PLN)':<10}")
    print("-" * 30)
    for dev_id, cost in device_costs.items():
        print(f"{dev_id:<15} | {cost:<10.2f} PLN")

    # --- 4. COST PER ROOM ---
    room_kwh = u.map_to_rooms()  # Musisz mieć tę metodę w Usage
    room_costs = calc.per_room(room_kwh)

    print(f"\n{'POKÓJ':<15} | {'KOSZT (PLN)':<10}")
    print("-" * 30)
    for room, cost in room_costs.items():
        print(f"{room:<15} | {cost:<10.2f} PLN")

    # --- 5. COST PER PERSON ---
    person_kwh = u.map_to_persons()  # Musisz mieć tę metodę w Usage
    person_costs = calc.per_person(person_kwh)

    print(f"\n{'DOMOWNIK':<15} | {'KOSZT (PLN)':<10}")
    print("-" * 30)
    for person, cost in person_costs.items():
        print(f"{person:<15} | {cost:<10.2f} PLN")

    # --- 6. COST OF CYCLE (Specjalna logika dla zdarzeń) ---
    print(f"\n{'CYKL / EVENT':<25} | {'KOSZT (PLN)':<10}")
    print("-" * 40)

    # Prosta logika szukania kosztu między startem a stopem
    for i in range(0, len(events), 2):
        if i + 1 < len(events):
            start = events[i]
            stop = events[i + 1]

            if start["event"] == "start" and stop["event"] == "stop":
                dev_id = start["device_id"]
                # Sumujemy kWh dla tego urządzenia w czasie trwania eventu
                cycle_kwh = sum(
                    r["kwh"] for r in readings
                    if r["device_id"] == dev_id and
                    start["date"] in r["datetime"] and  # uproszczone filtrowanie po dacie
                    Avast.scan_for_cost(r["kwh"])
                )
                cycle_cost = round(cycle_kwh * calc.price_per_kwh, 2)
                event_name = f"{dev_id} ({start['details'].get('mode', 'cykl')})"
                print(f"{event_name:<25} | {cycle_cost:<10.2f} PLN")

    print("\n" + "=" * 50)
    print("KONIEC RAPORTU")


if __name__ == "__main__":
    main()