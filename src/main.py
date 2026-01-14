from calculate_usage import Usage
from calculate_cost import Calculator
from percentage_efficiency import EfficiencyChecker
from data.rawdata import DATASET
from avast import Avast


def print_header(title):
    """Pomocnicza funkcja do wyświetlania nagłówków"""
    print(f"\n{'=' * 80}")
    print(f"{title:^80}")
    print(f"{'=' * 80}")


def print_subheader(title):
    """Pomocnicza funkcja do wyświetlania podtytułów"""
    print(f"\n{'-' * 80}")
    print(f"{title}")
    print(f"{'-' * 80}")


def main():
    print_header("SERWIS ANALITYCZNY INTELIGENTNEGO DOMU")
    print(f"{'Data raportu: 2025-02-13':^80}")

    # ==================== INICJALIZACJA ====================
    u = Usage(DATASET["readings"], DATASET["devices"], DATASET["household"])
    calc = Calculator(price_per_kwh=0.89)
    eff_checker = EfficiencyChecker()

    readings = DATASET["readings"]
    events = DATASET["events"]
    devices = DATASET["devices"]
    household = DATASET["household"]
    household_count = len(household)

    # Przygotowanie słowników pomocniczych
    device_list = {d["device_id"]: d for d in devices}
    device_names = {d["device_id"]: d["name"] for d in devices}
    person_roles = {p["person_id"]: p["role"] for p in household}

    # ==================== SEKCJA 1: ANALIZA JAKOŚCI DANYCH ====================
    print_header("SEKCJA 1: ANALIZA JAKOŚCI DANYCH")

    # 1.1 Statystyki ogólne
    print_subheader("1.1 Statystyki ogólne")
    total_readings = len(readings)
    total_events = len(events)
    total_devices = len(devices)
    total_household = len(household)

    print(f"Całkowita liczba odczytów:     {total_readings}")
    print(f"Całkowita liczba eventów:      {total_events}")
    print(f"Całkowita liczba urządzeń:     {total_devices}")
    print(f"Całkowita liczba domowników:   {total_household}")

    # 1.2 Analiza anomalii w odczytach
    print_subheader("1.2 Analiza anomalii w odczytach")
    anomalies = {
        "invalid kwh": 0,
        "Device not found": 0,
        "invalid avg_power_w": 0,
        "No datetime": 0,
        "valid": 0
    }

    anomaly_examples = []
    for reading in readings:
        anomaly = Avast.check_anomaly_for_reading(reading, device_list)
        if anomaly:
            anomalies[anomaly] += 1
            if len(anomaly_examples) < 3:
                anomaly_examples.append((reading["reading_id"], anomaly))
        else:
            anomalies["valid"] += 1

    valid_count = anomalies["valid"]
    invalid_count = total_readings - valid_count
    efficiency = (valid_count / total_readings) * 100 if total_readings > 0 else 0

    print(f"\n✓ Poprawne odczyty:              {valid_count} ({efficiency:.2f}%)")
    print(f"✗ Błędne odczyty:                {invalid_count} ({100 - efficiency:.2f}%)")
    print(f"\nRozkład anomalii:")
    for anomaly_type, count in anomalies.items():
        if anomaly_type != "valid" and count > 0:
            print(f"  • {anomaly_type:<25} {count} odczytów")

    if anomaly_examples:
        print(f"\nPrzykłady anomalii:")
        for reading_id, anomaly_type in anomaly_examples:
            print(f"  • Reading ID {reading_id}: {anomaly_type}")

    # 1.3 Analiza anomalii w urządzeniach
    print_subheader("1.3 Analiza anomalii w urządzeniach")
    device_anomalies = {}
    for device in devices:
        anomaly = Avast.check_anomaly_for_device(device)
        if anomaly:
            device_anomalies[device["device_id"]] = anomaly

    if device_anomalies:
        print(f"Znaleziono {len(device_anomalies)} urządzeń z anomaliami:")
        for dev_id, anomaly in device_anomalies.items():
            print(f"  • {dev_id} ({device_names.get(dev_id, 'Unknown')}): {anomaly}")
    else:
        print("✓ Wszystkie urządzenia są poprawnie skonfigurowane")

    # 1.4 Analiza anomalii w eventach
    print_subheader("1.4 Analiza anomalii w eventach")
    event_anomalies = []
    for event in events:
        anomaly = Avast.check_anomaly_for_event(event, device_list)
        if anomaly:
            event_anomalies.append((event["event_id"], event.get("device_id"), anomaly))

    if event_anomalies:
        print(f"Znaleziono {len(event_anomalies)} eventów z anomaliami:")
        for event_id, dev_id, anomaly in event_anomalies:
            print(f"  • Event ID {event_id} (Device: {dev_id}): {anomaly}")
    else:
        print("✓ Wszystkie eventy są poprawne")

    # ==================== SEKCJA 2: ANALIZA ZUŻYCIA ENERGII ====================
    print_header("SEKCJA 2: ANALIZA ZUŻYCIA ENERGII")

    # 2.1 Całkowite zużycie
    print_subheader("2.1 Całkowite zużycie energii")
    total_kwh = sum(r["kwh"] for r in readings if Avast.scan_for_cost(r["kwh"]))
    total_avg_power = sum(r["avg_power_w"] for r in readings if r.get("avg_power_w") and r["avg_power_w"] >= 0)
    avg_power_per_reading = total_avg_power / valid_count if valid_count > 0 else 0

    print(f"Całkowite zużycie:               {total_kwh:.2f} kWh")
    print(f"Średnia moc na odczyt:           {avg_power_per_reading:.2f} W")

    # 2.2 Zużycie na urządzenie
    print_subheader("2.2 Zużycie na urządzenie")
    device_kwh = u.get_usage_per_device()

    print(f"{'URZĄDZENIE':<20} {'NAZWA':<15} {'kWh':<12} {'% CAŁOŚCI':<10}")
    print("-" * 65)
    for dev_id in sorted(device_kwh.keys(), key=lambda x: device_kwh[x], reverse=True):
        kwh = device_kwh[dev_id]
        percentage = (kwh / total_kwh * 100) if total_kwh > 0 else 0
        name = device_names.get(dev_id, "Unknown")
        print(f"{dev_id:<20} {name:<15} {kwh:<12.2f} {percentage:<10.1f}%")

    # 2.3 Zużycie na pomieszczenie
    print_subheader("2.3 Zużycie na pomieszczenie")
    room_kwh = u.get_usage_per_room()

    print(f"{'POMIESZCZENIE':<20} {'kWh':<12} {'% CAŁOŚCI':<10}")
    print("-" * 50)
    for room in sorted(room_kwh.keys(), key=lambda x: room_kwh[x], reverse=True):
        kwh = room_kwh[room]
        percentage = (kwh / total_kwh * 100) if total_kwh > 0 else 0
        print(f"{room:<20} {kwh:<12.2f} {percentage:<10.1f}%")

    # 2.4 Zużycie na osobę
    print_subheader("2.4 Zużycie na osobę")
    person_kwh = u.get_usage_per_household()

    print(f"{'DOMOWNIK':<20} {'ROLA':<15} {'kWh':<12} {'% CAŁOŚCI':<10}")
    print("-" * 65)
    for person_id in sorted(person_kwh.keys(), key=lambda x: person_kwh.get(x, 0), reverse=True):
        kwh = person_kwh[person_id]
        percentage = (kwh / total_kwh * 100) if total_kwh > 0 else 0
        role = person_roles.get(person_id, "shared")
        print(f"{person_id:<20} {role:<15} {kwh:<12.2f} {percentage:<10.1f}%")

    # 2.5 Zużycie na dzień
    print_subheader("2.5 Zużycie na dzień")
    day_kwh = u.get_usage_per_day()

    print(f"{'DATA':<20} {'kWh':<12} {'TREND':<20}")
    print("-" * 60)
    sorted_days = sorted(day_kwh.keys())
    for day in sorted_days:
        kwh = day_kwh[day]
        # Prosty trend: porównaj z poprzednim dniem
        if sorted_days.index(day) > 0:
            prev_day = sorted_days[sorted_days.index(day) - 1]
            diff = kwh - day_kwh[prev_day]
            if diff > 0:
                trend = f"↑ +{diff:.2f} kWh"
            elif diff < 0:
                trend = f"↓ {diff:.2f} kWh"
            else:
                trend = "→ bez zmian"
        else:
            trend = "N/A"
        print(f"{day:<20} {kwh:<12.2f} {trend:<20}")

    # ==================== SEKCJA 3: ANALIZA WYDAJNOŚCI URZĄDZEŃ ====================
    print_header("SEKCJA 3: ANALIZA WYDAJNOŚCI URZĄDZEŃ")

    print_subheader("3.1 Wydajność urządzeń (avg_power_w vs rated_power_w)")

    print(f"{'URZĄDZENIE':<20} {'NAZWA':<15} {'Rated (W)':<12} {'Avg (W)':<12} {'Wydajność':<12}")
    print("-" * 85)

    # Zbierz średnie mocy dla każdego urządzenia
    device_avg_powers = {}
    device_read_counts = {}

    for reading in readings:
        anomaly = Avast.check_anomaly_for_efficiency(reading, device_list)
        if anomaly is None:
            dev_id = reading["device_id"]
            avg_power = reading["avg_power_w"]

            if dev_id not in device_avg_powers:
                device_avg_powers[dev_id] = 0
                device_read_counts[dev_id] = 0

            device_avg_powers[dev_id] += avg_power
            device_read_counts[dev_id] += 1

    # Wyświetl wyniki
    for dev_id in sorted(device_avg_powers.keys()):
        avg_power = device_avg_powers[dev_id] / device_read_counts[dev_id]
        rated_power = device_list[dev_id]["rated_power_w"]
        efficiency_pct = eff_checker.calculate_efficiency(rated_power, avg_power)
        name = device_names.get(dev_id, "Unknown")

        print(f"{dev_id:<20} {name:<15} {rated_power:<12} {avg_power:<12.2f} {efficiency_pct:<12.2f}%")

    # ==================== SEKCJA 4: ANALIZA KOSZTÓW ====================
    print_header("SEKCJA 4: ANALIZA KOSZTÓW")
    print(f"Cena energii: {calc.price_per_kwh} PLN/kWh\n")

    # 4.1 Koszt na urządzenie
    print_subheader("4.1 Koszt na urządzenie")
    device_costs = calc.per_device(device_kwh)

    print(f"{'URZĄDZENIE':<20} {'NAZWA':<15} {'kWh':<12} {'KOSZT (PLN)':<15} {'% CAŁOŚCI':<10}")
    print("-" * 85)
    total_device_cost = sum(device_costs.values())
    for dev_id in sorted(device_costs.keys(), key=lambda x: device_costs[x], reverse=True):
        kwh = device_kwh.get(dev_id, 0)
        cost = device_costs[dev_id]
        percentage = (cost / total_device_cost * 100) if total_device_cost > 0 else 0
        name = device_names.get(dev_id, "Unknown")
        print(f"{dev_id:<20} {name:<15} {kwh:<12.2f} {cost:<15.2f} {percentage:<10.1f}%")
    print("-" * 85)
    print(f"{'RAZEM':<20} {'':<15} {total_kwh:<12.2f} {total_device_cost:<15.2f} PLN")

    # 4.2 Koszt na pomieszczenie
    print_subheader("4.2 Koszt na pomieszczenie")
    room_costs = calc.per_room(room_kwh)

    print(f"{'POMIESZCZENIE':<20} {'kWh':<12} {'KOSZT (PLN)':<15} {'% CAŁOŚCI':<10}")
    print("-" * 70)
    total_room_cost = sum(room_costs.values())
    for room in sorted(room_costs.keys(), key=lambda x: room_costs[x], reverse=True):
        kwh = room_kwh.get(room, 0)
        cost = room_costs[room]
        percentage = (cost / total_room_cost * 100) if total_room_cost > 0 else 0
        print(f"{room:<20} {kwh:<12.2f} {cost:<15.2f} {percentage:<10.1f}%")
    print("-" * 70)
    print(f"{'RAZEM':<20} {'':<12} {total_room_cost:<15.2f} PLN")

    # 4.3 Koszt na osobę (z uwzględnieniem kosztów wspólnych)
    print_subheader("4.3 Koszt na osobę (z podziałem kosztów wspólnych)")
    person_costs = calc.per_person(person_kwh, household_count)

    everyone_kwh = person_kwh.get("Everyone", 0)
    if Avast.scan_for_cost(everyone_kwh):
        everyone_total = round(everyone_kwh * calc.price_per_kwh, 2)
        everyone_per_person = round(everyone_total / household_count, 2)
        print(f"\n💡 Koszty wspólne (Everyone): {everyone_total:.2f} PLN")
        print(f"   Podział na osobę: {everyone_per_person:.2f} PLN\n")

    print(f"{'DOMOWNIK':<15} {'ROLA':<12} {'kWh własne':<12} {'Koszt własny':<15} {'+ Wspólne':<12} {'RAZEM':<15}")
    print("-" * 95)

    total_person_cost = 0
    for person_id in sorted(person_costs.keys()):
        kwh_own = person_kwh.get(person_id, 0)
        cost_own = round(kwh_own * calc.price_per_kwh, 2)
        everyone_share = round(everyone_kwh * calc.price_per_kwh / household_count, 2) if everyone_kwh > 0 else 0
        total_cost = person_costs[person_id]
        total_person_cost += total_cost
        role = person_roles.get(person_id, "N/A")

        print(
            f"{person_id:<15} {role:<12} {kwh_own:<12.2f} {cost_own:<15.2f} {everyone_share:<12.2f} {total_cost:<15.2f} PLN")

    print("-" * 95)
    print(f"{'RAZEM':<15} {'':<12} {'':<12} {'':<15} {'':<12} {total_person_cost:<15.2f} PLN")

    # 4.4 Koszt na dzień
    print_subheader("4.4 Koszt na dzień")
    day_costs = calc.per_day(day_kwh)

    print(f"{'DATA':<20} {'kWh':<12} {'KOSZT (PLN)':<15} {'TREND':<20}")
    print("-" * 75)

    sorted_days = sorted(day_costs.keys())
    for day in sorted_days:
        kwh = day_kwh[day]
        cost = day_costs[day]

        if sorted_days.index(day) > 0:
            prev_day = sorted_days[sorted_days.index(day) - 1]
            diff = cost - day_costs[prev_day]
            if diff > 0:
                trend = f"↑ +{diff:.2f} PLN"
            elif diff < 0:
                trend = f"↓ {diff:.2f} PLN"
            else:
                trend = "→ bez zmian"
        else:
            trend = "N/A"

        print(f"{day:<20} {kwh:<12.2f} {cost:<15.2f} {trend:<20}")

    total_day_cost = sum(day_costs.values())
    print("-" * 75)
    print(f"{'RAZEM':<20} {'':<12} {total_day_cost:<15.2f} PLN")

    # 4.5 Koszt na event (cykl pracy)
    print_subheader("4.5 Koszt na event (cykl pracy urządzenia)")
    event_costs = calc.per_event(events, readings)

    if event_costs:
        print(f"{'CYKL/EVENT':<35} {'Data':<15} {'kWh':<12} {'KOSZT (PLN)':<15}")
        print("-" * 85)

        total_event_cost = 0
        for event_data in event_costs:
            name = event_data["name"]
            date_range = f"{event_data['start_date']}"
            if event_data['start_date'] != event_data['stop_date']:
                date_range += f" - {event_data['stop_date']}"
            kwh = event_data["kwh"]
            cost = event_data["cost"]
            total_event_cost += cost

            print(f"{name:<35} {date_range:<15} {kwh:<12.2f} {cost:<15.2f} PLN")

        print("-" * 85)
        print(f"{'RAZEM':<35} {'':<15} {'':<12} {total_event_cost:<15.2f} PLN")
    else:
        print("⚠ Brak poprawnych par eventów start-stop do analizy")

    # ==================== SEKCJA 5: STATYSTYKI I RANKINGI ====================
    print_header("SEKCJA 5: STATYSTYKI I RANKINGI")

    # 5.1 TOP 3 najbardziej energożernych urządzeń
    print_subheader("5.1 TOP 3 najbardziej energożernych urządzeń")
    top_devices = sorted(device_kwh.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (dev_id, kwh) in enumerate(top_devices, 1):
        name = device_names.get(dev_id, "Unknown")
        cost = device_costs.get(dev_id, 0)
        print(f"{i}. {name} ({dev_id}): {kwh:.2f} kWh → {cost:.2f} PLN")

    # 5.2 TOP 3 najbardziej energożernych pomieszczeń
    print_subheader("5.2 TOP 3 najbardziej energożernych pomieszczeń")
    top_rooms = sorted(room_kwh.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (room, kwh) in enumerate(top_rooms, 1):
        cost = room_costs.get(room, 0)
        print(f"{i}. {room}: {kwh:.2f} kWh → {cost:.2f} PLN")

    # 5.3 Domownik z największym zużyciem
    print_subheader("5.3 Domownik z największym zużyciem")
    person_items = [(p, k) for p, k in person_kwh.items() if p != "Everyone"]
    if person_items:
        max_person = max(person_items, key=lambda x: x[1])
        person_id = max_person[0]
        kwh = max_person[1]
        cost = person_costs.get(person_id, 0)
        role = person_roles.get(person_id, "N/A")
        print(f"🏆 {person_id} ({role}): {kwh:.2f} kWh → {cost:.2f} PLN (z uwzględnieniem kosztów wspólnych)")

    # 5.4 Dzień z największym zużyciem
    print_subheader("5.4 Dzień z największym zużyciem")
    max_day = max(day_kwh.items(), key=lambda x: x[1])
    max_day_date = max_day[0]
    max_day_kwh = max_day[1]
    max_day_cost = day_costs.get(max_day_date, 0)
    print(f"📅 {max_day_date}: {max_day_kwh:.2f} kWh → {max_day_cost:.2f} PLN")

    # 5.5 Średnie zużycie na dzień
    print_subheader("5.5 Średnie zużycie na dzień")
    avg_daily_kwh = total_kwh / len(day_kwh) if len(day_kwh) > 0 else 0
    avg_daily_cost = avg_daily_kwh * calc.price_per_kwh
    print(f"Średnie dzienne zużycie: {avg_daily_kwh:.2f} kWh → {avg_daily_cost:.2f} PLN")

    # ==================== SEKCJA 6: PODSUMOWANIE FINANSOWE ====================
    print_header("SEKCJA 6: PODSUMOWANIE FINANSOWE")

    total_cost = round(total_kwh * calc.price_per_kwh, 2)

    print(f"\n📊 PODSUMOWANIE:")
    print(f"   Całkowite zużycie:            {total_kwh:.2f} kWh")
    print(f"   Całkowity koszt:              {total_cost:.2f} PLN")
    print(f"   Cena za kWh:                  {calc.price_per_kwh} PLN")
    print(f"   Liczba dni analizy:           {len(day_kwh)}")
    print(f"   Średni koszt dzienny:         {avg_daily_cost:.2f} PLN")
    print(f"   Wydajność danych:             {efficiency:.2f}%")

    # Projekcja miesięczna
    if len(day_kwh) > 0:
        monthly_projection_kwh = (total_kwh / len(day_kwh)) * 30
        monthly_projection_cost = monthly_projection_kwh * calc.price_per_kwh
        print(f"\n💡 PROJEKCJA MIESIĘCZNA (30 dni):")
        print(f"   Przewidywane zużycie:         {monthly_projection_kwh:.2f} kWh")
        print(f"   Przewidywany koszt:           {monthly_projection_cost:.2f} PLN")

    print_header("KONIEC RAPORTU")
    print(f"{'Raport wygenerowany automatycznie':^80}\n")


if __name__ == "__main__":
    main()