import numpy as np
import matplotlib.pyplot as plt
import pykep as pk

# '''
#     Beam_Search:
#     0.  INIT-FUNKTION

#     1.  Funktion: Daten aufrufen
#     2.  Funktion: Cluster für X Knoten erstellen --> Cluster eps < Delta_V --> Zeitbereich  ==> Im Cluster sind Y > X neue Asteoriden (!! Keine doppelten Asteoriden)
#     3.  X   Zeitoptimierung (Basti)
#     4.  Beam-Search:
#         4.1.    Lambert-Problem oder Approximativ für Delta_V 
#         4.2.    Rostoff-Minimum abfragen    --> bereits Bevorzugung einbauen minimalen Rohstoff vs. Tank
#         4.3.    Cluster bilden nur aus gewissen Rohstoffen (bevorzugt minimaler Rohstoff)
#         4.4.    X   Entscheidungsfunktion   --> was müssen Ein- & Ausgang sein?     (Mathias)
#     5.  Abflug- & Ankunftszeitpunkt berechnen für Zeitplan
    
# '''
################
### Constants
################

# Start and end epochs
T_START = pk.epoch_from_iso_string("30190302T000000")
T_END = pk.epoch_from_iso_string("30240302T000000")
T_CURRENT = 0
T_CURRENT_e = pk.epoch(0)
G = 6.67430e-11                                 # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30                                   # Sun_mass (kg)
MS = 8.98266512e-2 * SM                         # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS                            # Mu of the Trappist-1 star
DV_per_propellant = 10000                       # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30                         # Maximum time to fully mine an asteroid
PROPELLANT = 1.0
STORAGE = []
VISITED = []


# # 1. Daten laden & "sortieren" für Benutzung
# data = np.loadtxt('C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_Guertelgold/SpoC_Projekt/SpoC_Datensatz.txt')
# asteroids = []
# for line in data:
#     p = pk.planet.keplerian(
#         T_START,
#         (
#             line[1],
#             line[2],
#             line[3],
#             line[4],
#             line[5],
#             line[6],
#         ),
#         MU_TRAPPIST,
#         G * line[7],  # mass in planet is not used in UDP, instead separate array below
#         1,  # these variable are not relevant for this problem
#         1.1,  # these variable are not relevant for this problem
#         "Asteroid " + str(int(line[0])),
#     )
#     asteroids.append(p)

# # And asteroids' masses and material type
# asteroid_masses = data[:, -2]
# asteroid_materials = data[:, -1].astype(int)


# # 2. Delta-V berechnen über Lambert?
# ##### Sagen wir, wir haben 2 Asteroiden gegeben --> Delta-V davon berechnen

# def calc_Delta_V(asteroid1_id, asteroid2_id, t_limit=20):
#     """S
#     - asteroid1_id:    ID vom Start-Asteroiden, von dem der neue Flug/Sprung ausgeht
#     - asteroid2_id:    ID vom durchs Optimierungsverfahren ausgewählten Asteroiden
#     - t_limit:          Gibt das Zeitfenster an, welches für einen Transfer überhaupt in Frage kommt
#     """
    
#     asteroid1_id = int(asteroid1_id)
#     asteroid2_id = int(asteroid2_id)

#     for i in VISITED:
#         if asteroid1_id not in VISITED:
#             VISITED.append(asteroid1_id)
#         if asteroid2_id not in VISITED:
#             VISITED.append(asteroid2_id)

#     # Iteration über der Zeit:
#     for t in np.linspace(0, t_limit,10):
#         tof = t - T_CURRENT
#         if tof < 0: tof = 0

#         # Infos zu Start-Asteroid:
#         r1, v1 = asteroids[asteroid1_id].eph(T_CURRENT_e)
#         # Infos zu Ziel-Asteroid:
#         r2, v2 = asteroids[asteroid2_id].eph(t)

#         l = pk.lambert_problem(r1=r1, r2=r2, tof=tof * pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0) # Time of flight kontrollieren

#         # Compute the delta-v necessary to go there and match its velocity
#         DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
#         DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
#         DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)

#         # Nach Flug noch vorhandener Kraftstoff
#         propellant = PROPELLANT - DV / DV_per_propellant
    
#     return(DV, propellant) # + time of arrival ==> ZEITEN KONTROLLIEREN & BESSER EINBAUEN
# # ==> Die übergebene Zeit ist kein Limit, sondern dann schon das berechnete Zeitoptimum!
# # ==> ACHTUNG: Delta_V muss schon unbedingt berechnet worden sein, dh ich brauche den Code grundlegend nicht, sondern kann direkt drauf zugreifen
    
# def calc_prepared_material(asteroid_id, t):
#     """
#     - asteroid:        Aktueller Asteroid
#     - t:               Verweildauer auf Asteroid1, bestimmt durch Zeitoptimierung

#     """
#     if asteroids[asteroid_id[:,-1].astype(int)] == 3:
#         STORAGE[asteroids[asteroid_id[:,-1].astype(int)]] = np.minimum(1.0, t * asteroids[asteroid_id[:,-2]] / TIME_TO_MINE_FULLY)
#     STORAGE[asteroids[asteroid_id[:,-1].astype(int)]] += t * asteroids[asteroid_id[:,-2]] / TIME_TO_MINE_FULLY       # pro Tag 1/30 abbaubar

#     return (STORAGE)
# # ==> ACHTUNG: Beim Propellant gibt es auch ein Maximum!! 


# # ==> Noch eine Funktion, die den prozentualen Anteil der Rohstoffe ausgibt

# def calc_minimum():
#     return(
#         STORAGE.index(np.min(STORAGE))
#     )

# # ==> Propellant separat betrachten



# # ==> Funktion, um Asteroidenfeld zu analysieren --> most valuable material
#     # (Tank)
#     # Bestand
#     # Masse



# def clustering():
#     return()

# print(calc_Delta_V(data[0,0], data[1,0]))
# # print(data[0,0])



#######################################################################################
#### Mathias: Alles normiert von 0 bis 1 und 2 Nachkommastellen in 0,01er-Schritten ###
#######################################################################################

_datenpfad = np.loadtxt('C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_Guertelgold/SpoC_Projekt/SpoC_Datensatz.txt')

class PSA_experiments():
    """ Grundgerüst für das PSA Gürtelgold
    
    """

    def __init__(self,data) :
        """
        Parameter:
        -   data:   Datenpfad als txt-Datei übergeben
        """
        self.data = data
        self.materials = materials
        pass

    def load_data(self,i):
        """
        Laden der Daten und sortieren für die Anwendung über Keppler-Paramerter zB.
        """

        asteroids = []
        for line in self.data:
            p = pk.planet.keplerian(
                T_START,
                (
                    line[1],
                    line[2],
                    line[3],
                    line[4],
                    line[5],
                    line[6],
                ),
                MU_TRAPPIST,
                G * line[7],  # mass in planet is not used in UDP, instead separate array below
                1,  # these variable are not relevant for this problem
                1.1,  # these variable are not relevant for this problem
                "Asteroid " + str(int(line[0])),
            )
            asteroids.append(p)

        asteroid_masses = self.data[i, -2]
        asteroid_materials = self.data[i, -1].astype(int)

    def asteroid_mass(self,i):
        """ Rückgabe:   Masse von Asteroid i"""
        return(self.data[i, -2])

    def material_stock(self):
        pass

    def asteroid_material(self,i):
        """Rückgabe:    Material von Asteroid i"""
        return(self.data[i, -1].astype(int))
        
    def DV_lambert(self):
        pass

    def DV_orbital(self):
        pass



- Bestand der Materialien (wie ich das gemacht hab ist, ich hab den materialtyp vom asteroid abgefragt, dann die anzahl von diesem material die ich schon hab / gesammt masse von mat den ich hab)
- delta v, bzw spritverbrauch
- masse vom asteroid


    

    def Stundeplan(self):
        pass






class Zeitoptimierung:  # Sebastian
    pass

class Asteroidenwahl:   # Mathias
    pass

class Asteroidensprung:

    def __init__(self, asteroid1, asteroid2) -> None:
        """
        Parameter:
        -   asteroid1:  Asteroid 1 als Vektor
        -   asteroid2:  Asteroid 2 als Vektor
        """
        self.x1 = asteroid1

        pass

