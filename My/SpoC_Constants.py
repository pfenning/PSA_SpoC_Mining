import numpy as np
# import numpy.ma as ma
import pykep as pk

from Moduls.fuzzy_system import FuzzySystem

#########################
# Static Class Constants
#########################
T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
T_DAUER = 1827
G = 6.67430e-11  # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30  # Sun_mass (kg)
MS = 8.98266512e-2 * SM  # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS  # Mu of the Trappist-1 star
DV_per_propellant = 10000  # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30  # Maximum time to fully mine an asteroid


#################
# ASTEROIDS:  Creating lists with indices of asteroids
#################

# Loading data as keplerian elements (planets) in an "array"
data = np.loadtxt("Asteroidengürtel.txt")
dict_asteroids ={int(line[0]):  # ID
    [pk.planet.keplerian(       # Keplerian-Object
        T_START,
        (
            line[1],
            line[2],
            line[3],
            line[4],
            line[5],
            line[6]
        ),
        MU_TRAPPIST,
        G * line[7],    # mass in planet is not used in UDP, instead separate array below
        1,              # these variable are not relevant for this problem
        1.1,            # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0]))),
        line[-2],               # Mass
        int(line[-1])]          # Material
    for line in data}

def verfuegbarkeit():
    """
    Berechnet die ursprüngliche Verfügbarkeit der Materialien
    """
    material = data[:,-1]
    mass = data[:,-2]
    gesamt = np.sum(mass)
    verf = [0, 0, 0, 0]
    for i in range(0,len(material)):
        if material[i] == 0:
            verf[0] += mass[i]
        elif material[i] == 1:
            verf[1] += mass[i]
        elif material[i] == 2:
            verf[2] += mass[i]
        elif material[i] == 3:
            verf[3] += mass[i]
    # print(verf)
    verf_norm = verf/gesamt
    return np.array(verf_norm), np.argmin(verf_norm)

#########
# GÜTE
#########
verf, material_most_needed = verfuegbarkeit()
# print(f"Verfügbarkeit der Materialien:{verf}")
# print(f"Bestmögliches Gütemass:{norm_material}")
my_system = FuzzySystem(verf.min(), verf.max(), resolution=0.01)


def get_t_opt(asteroid_id, prop_needed=None):
    """
    Bestimmt die Abbauzeit, um die gesamte Asteroidenmasse abzubauen.
    Für Tank-Asteroiden wird die Zeit bestimmt, die benötigt wird, um Tank abzubauen, falls diese geringer ist
    als die Standard-Abbauzeit
    :param prop_needed: fehlender Treibstoff
    :param asteroid_id: abzubauender Asteroiden
    :return: Abbauzeit
    """
    if prop_needed is None or get_asteroid_mass(asteroid_id) < prop_needed:
        return get_asteroid_mass(asteroid_id)*TIME_TO_MINE_FULLY
    else:
        return prop_needed*TIME_TO_MINE_FULLY

def get_asteroid(asteroid_id):
    """
    Gibt das Kaplerian-Objekt des Asteroiden zurück
    :param asteroid_id: Asteroid-ID
    :return: Kaplerian-Objekt des Asteroidn
    """
    return dict_asteroids[asteroid_id][0]

def get_asteroid_mass(asteroid_id):
    """
    Bestimmt die Masse des Asteroiden
    :param asteroid_id: Asteroid-ID
    :return: Masse des Asteroiden
    """
    return dict_asteroids[asteroid_id][1]

def get_asteroid_material(asteroid_id):
    """
    Bestimmt das Material des Asteroiden
    :param asteroid_id: Asteroid-ID
    :return: Material des Asteroiden
    """
    return dict_asteroids[asteroid_id][2]

def norm_bestand(bestand, material):
    """
    Gibt "normierten" Bestand zurück.
    Für Rohstoffe: 1/max(Rohstoffe)
    Für Tank: Tank
    :param bestand: Aktueller bestand der 3 Rohstoffe und des Tanks
    :param material: zu normierendes Material
    :param norm_material: Normierung für Bestand der Materialien
    :return: "normierter" Bestand
    """
    if material == 3:
        return bestand[3]
    elif max(bestand[:3]) == 0:
        return 0
    else:
        return bestand[material]/max(bestand[:3])


def get_dv(asteroid1, asteroid2, t_start, t_flug, print_result=False):
    """
    Berechnung des approximierten Delta V mithilfe des Lambert-Problems
    :param asteroid1: Start-Asteroid
    :param asteroid2: Lande-Asteroid
    :param t_start: Startzeitpunkt
    :param t_flug: Flugzeit
    :param print_result: Ausgabe des Ergebnisses mit print()
    :return: Delta V für berechnete Flugbahn
    """
    r1, v1 = asteroid1.eph(
        T_START.mjd2000 + t_start
    )
    r2, v2 = asteroid2.eph(
        T_START.mjd2000 + t_start + t_flug
    )
    # Solve the lambert problem for this flight
    l = pk.lambert_problem(
        r1=r1, r2=r2, tof=t_flug * pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0
    )
    # Compute the delta-v necessary to go there and match its velocity
    dv1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
    dv2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
    DV = np.linalg.norm(dv1) + np.linalg.norm(dv2)

    if print_result:
        print("Starttag:", f"{t_start:.0f}", "Flugzeit:", f"{t_flug:.0f}", " => Delta V =", f"{DV:.0f}")

    return DV


def clustering(knn, asteroids_kp, asteroid_1_idx, radius=4000):
    """
    Clusterbildung um Asteroid herum
    :param knn: Cluster for "asteroids_kp"
    :param asteroids_kp: Index-Liste von allen Asteroiden
    :param asteroid_1_idx: Index vom aktuellen Asteroiden
    :param radius: Begrenzung des Clusters auf max. Radius
    :return: IDs der Nachbarn
    """
    neighb, neighb_inds, neighb_dis = knn.find_neighbours(asteroids_kp[asteroid_1_idx], query_type='ball', r=radius)
    neighb_inds = list(neighb_inds)
    return neighb_inds


# ToDo: Zeitraum der Flugzeit neu definieren (z.B. auf 5-46 in 4er Schritten)
#       - Reicht Auflösung? Sonst: nach gefundenem Minimum nochmal einen halben Schritt in jede Richtung machen
def time_optimize(asteroid1, asteroid1_mas, asteroid1_mat,
                  asteroid2, t_arr, t_opt, limit=1.0, print_result=False,
                  needed=False,
                  time_divider = 20,
                  alpha=1):
    """
    Zeitoptimierung von Delta V mit 2 Levels. Erst Flugzeit, dann Startzeit

    Unterschied zu v1:
    Betrachteter Startpunkt bewegt sich bis zu 60 Tage.
    Wenn Material dringend benötigt wird, wird mit Abflug gewartet, bis es komplett abgebaut wurde
    Auswahl des Minimums über Gewichtung der Größen Flugzeit, Abbauzeit, Spritverbrauch

    Übergabe: Asteroid 1 und 2, optimaler Startpunkt, optimale Abbauzeit auf aktuellem Asteroiden
    Rückgabe: optimaler Startpunkt, optimale Flugzeit, optimiertes DV
    :param asteroid1_mas:   Masse von Asteroid 1
    :param asteroid1_mat:   Material von Asteroid 1
    :param asteroid1:       Startasteroid
    :param asteroid2:       Landeasteroid
    :param t_arr:           Ankunftstag auf Asteroid 1
    :param t_opt:           Abbauzeit, um aktuellen Asteroid vollständig abzubauen
    :param limit:           maximal erlaubter Tank
    :param print_result:    Ergebnisse von get_dv für das 2. Level der Optimierung ausgeben
    :param needed:          Wichtigkeit des Materials
    :param time_divider:    wie start t_flug gewichtet wird (größer = weicher)
    :return: alpha gewählte Starttage, gewählte Flugzeiten, sich ergebene DVs
    """
    t_start = t_arr+t_opt

    ###################################################
    # Variation der Flugzeit, Startpunkt fest
    ###################################################
    if print_result:
        print("==== Auswahl der Flugzeit ====")
        print(" T |  DV  | Score")
    # Variation der Flugzeit
    t_flug_v = range(2, 30, 2)
    # Variation des Abflugtags
    if needed or t_opt < 2.1:
        t_start_var = []
    else:
        t_start_var = - np.arange(1, 0.3*t_opt, 2)  # => [.... , -5, -3, -1]
    # Nach optimalem Startpunkt
    t_start_var = np.concatenate([t_start_var, np.arange(0, 60 - t_opt, 4)], axis=0)
    t_flug_map, t_start_var_map = np.meshgrid(t_flug_v, t_start_var, indexing='ij')
    dv_map = np.zeros((len(t_flug_v), len(t_start_var)))
    costs = np.zeros_like(dv_map)
    count = 0
    for i, t_flug in enumerate(t_flug_v):
        for j, t_var in enumerate(t_start_var):
            # Sprit berechnen
            dv_map[i][j] = get_dv(asteroid1, asteroid2, t_start+t_var, t_flug)
            # Score berechnen
            if dv_map[i][j]/DV_per_propellant < limit:
                count += 1
                costs[i][j] = 0.3 * t_flug / 22 \
                              + 0.2 * 10000/2100 * dv_map[i][j]/(10000 - dv_map[i][j]) \
                              + 0.3 * abs(t_start_var[j])/7
                if 100 < costs[i][j]:
                    costs[i][j] = 99
            else:
                costs[i][j] = 100 # Muss nur größer sein als alle realistischen Ergebnisse von darüber
    # Minimum auswählen
    t_flug_min_dv = []
    t_m_min_dv = []
    dv_min = []
    if count < alpha:
        alpha = int(count)
    index_pairs = [np.unravel_index(i, costs.shape) for i in np.argpartition(costs.flatten(), alpha)[:alpha]]
    for i,j in index_pairs:
        t_flug_min_dv.append(t_flug_v[i])
        t_m_min_dv.append(t_opt + t_start_var[j])
        dv_min.append(dv_map[i][j])

    if print_result:
        print("==== Auswahl des Starttags ====")
        print(f"Optimale Abbauzeit:{t_opt:.1f}, Needed:{needed}")
        print(" delta Start | Flugzeit |  DV  | Score")
        for i, t_flug in enumerate(t_flug_v):
            for j, t_var in enumerate(t_start_var):
                print(f"{t_var:0f} | {t_flug:0f} | {dv_map[i][j]:.0f} | {costs[i][j]:.2f}")
        print(f"Gewähltes Ergebnise: ")
        for t_m, t_flug, dv in zip(t_m_min_dv, t_flug_min_dv, dv_min):
            print(f"{t_m-t_opt:.0f}, {t_flug:.0f}, {dv:.0f}")

    return t_m_min_dv, t_flug_min_dv, dv_min


def abbau(bestand, mass, material, t_m):
    """
    Berechnung des abgebauten Materials und Bearbeitung von Bestand entsprechend
    :param mass: Masse des Asteroiden
    :param bestand: derzeitiger Bestand
    :param material: Material-Index
    :param t_m: Aufenthaltsdauer auf Planet
    :return:
    """
    if t_m<0:
        return
    bestand[material] = get_abbau_menge(bestand[material], mass, material, t_m)


def get_abbau_menge(material_bestand, mass, material, t_m):
    """
    Berechnet die Abbaumenge für ein übergebenes Material und addiert es auf den Bestand
    :param material_bestand: aktueller Bestand des Materials
    :param mass: Masse des Asteroiden
    :param material: Material-Typ
    :param t_m: Aufenthaltszeit auf Asteroiden
    :return: neuer Bestand des Materials
    """
    if material == 3:
        propellant_found = np.minimum(mass, (t_m / TIME_TO_MINE_FULLY))
        material_bestand = np.minimum(1.0, material_bestand + propellant_found)
    else:
        material_bestand += np.minimum(mass, (t_m / TIME_TO_MINE_FULLY))

    return material_bestand


def sort_vector(vec_1, vec_2):

    vec_1_neu = vec_1
    vec_2_neu = vec_2

    return vec_1_neu, vec_2_neu