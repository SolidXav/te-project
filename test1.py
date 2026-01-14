import sys
import os

# --- 1. KONFIGURACJA ŚRODOWISKA (FIX DLA FOLDERU PACKAGES) ---
# Ustawiamy ścieżkę tak, aby Python widział Twój folder 'packages'
current_dir = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.join(current_dir, 'packages')

if os.path.exists(packages_dir):
    # Wstawiamy na początek listy (indeks 0), aby mieć priorytet
    sys.path.insert(0, packages_dir)

# --- 2. IMPORT BIBLIOTEK ---
try:
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    print("Biblioteki załadowane pomyślnie!")
except ImportError as e:
    print(f"BŁĄD IMPORTU: {e}")
    print("Sprawdź czy folder 'packages' znajduje się w tym samym miejscu co ten plik.")
    sys.exit(1)

# --- 3. GENEROWANIE PRZYKŁADOWYCH DANYCH (SYMULACJA) ---
# Tworzymy dane przypominające odczyty z inteligentnego domu
np.random.seed(42)  # Stałe ziarno losowości (żeby wykres zawsze wyglądał tak samo)

# Dni tygodnia i godziny
days = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
hours = list(range(24))

data = []
for day in days:
    for hour in hours:
        # Bazowe zużycie (losowe szumy)
        consumption = np.random.normal(loc=100, scale=30)

        # Dodajemy logikę: Rano (7-9) i Wieczór (18-22) jest większe zużycie
        if 7 <= hour <= 9:
            consumption += 150  # Ranny szczyt (śniadanie, szykowanie się)
        elif 18 <= hour <= 22:
            consumption += 250  # Wieczorny szczyt (TV, światło, gotowanie)

        # W weekendy (Sob, Nd) zużycie jest wyższe w środku dnia
        if day in ['Sobota', 'Niedziela'] and 10 <= hour <= 16:
            consumption += 100

        data.append({'Dzień': day, 'Godzina': hour, 'Zużycie [W]': max(0, consumption)})

# Tworzymy DataFrame (tabelę)
df = pd.DataFrame(data)

# --- 4. TWORZENIE ZAAWANSOWANEGO WYKRESU (HEATMAP) ---
print("Generowanie wykresu...")

# Pivot table: Przekształcamy dane w macierz (Wiersze=Dni, Kolumny=Godziny)
heatmap_data = df.pivot(index="Dzień", columns="Godzina", values="Zużycie [W]")
# Sortujemy dni tygodnia w poprawnej kolejności
heatmap_data = heatmap_data.reindex(days)

# Ustawienia stylu
sns.set_theme(style="whitegrid")  # Ładniejszy styl tła
plt.figure(figsize=(14, 8))  # Duży rozmiar wykresu

# Rysowanie Mapy Ciepła
# cmap="YlOrRd" -> Kolory od Żółtego (mało) przez Pomarańczowy do Czerwonego (dużo)
ax = sns.heatmap(heatmap_data, cmap="YlOrRd", annot=False, linewidths=.5, cbar_kws={'label': 'Średnia Moc [W]'})

# --- 5. KOSMETYKA WYKRESU ---
plt.title('Profil Zużycia Energii w Domu (Symulacja)', fontsize=16, pad=20)
plt.ylabel('Dzień Tygodnia', fontsize=12)
plt.xlabel('Godzina Dnia', fontsize=12)

# Dodanie adnotacji tekstowej na wykresie
plt.text(12, 7.5, 'Weekendowy wzrost aktywności', ha='center', color='blue', fontsize=10, weight='bold')

# Wyświetlenie
print("Wyświetlanie okna z wykresem...")
plt.tight_layout()
plt.show()