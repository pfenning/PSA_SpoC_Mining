from fuzzy_system import FuzzySystem
import time

# Timer "starten"
time0 = time.perf_counter()

my_system = FuzzySystem(0.03, 0.4, resolution=0.02)
time1 = time.perf_counter()
time_Variante1 = time1-time0

str_cal = my_system.calculate_score(
    t_n=0.4,
    delta_v=0.2,
    bes=0.2,
    verf=0.1,
    mas=0.9)
time2 = time.perf_counter()
time_Variante2 = time2-time1

# Berechnung mit Kennfeld (noch viel zu langsame Berechnung von Kennfeld)
my_system.initialize_map_calculation(calculate_new=True)
# my_system.load_maps_from_npy()
time3 = time.perf_counter()
time_Variante3 = time3-time2

map_cal = my_system.calculate_score_by_map(
    t_n=0.4,
    delta_v=0.2,
    bes=0.2,
    verf=0.1,
    mas=0.9)
time4 = time.perf_counter()
time_Variante4 = time4-time3

print(f"Berechnung mit Standardverfahren: {str_cal:.2}")
print(f"Berechnung mit Kennfeld: {map_cal:.2}")
print(f"Fehler der Berechnung: {abs(str_cal-map_cal):.3}")
print(f"Initialisierung des Systems: {time_Variante1:.5}")
print(f"Abfrage mit Standardverfahren: {time_Variante2:.5}")
print(f"Erstellen des Kennfeldes: {time_Variante3:.5}")
print(f"Abfrage des Kennfeldes: {time_Variante4:.5}")
print(f"Abfragezeit Standard / Abfragezeit Map = {time_Variante2/time_Variante4:.3}")

