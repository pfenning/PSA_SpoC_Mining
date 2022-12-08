import numpy as np
import matplotlib.pyplot as plt
import pykep as pk

################
### Constants
################
T_START = pk.epoch_from_iso_string("30190302T000000")   # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
G = 6.67430e-11                                 # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30                                   # Sun_mass (kg)
MS = 8.98266512e-2 * SM                         # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS                            # Mu of the Trappist-1 star
DV_per_propellant = 10000                       # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30                         # Maximum time to fully mine an asteroid


####################
### Laufvariablen       ==> sellten in self gespeichert werden
####################
t_current = 0
t_current_e = pk.epoch(0)
t_left = 1827 - t_current
t_spent = [0] # prepping material
t_arrival = [0]
propellant = 1.0
asteroids = []
visited = []
sugg = []                   # hier nicht addieren, immer neu löschen...dann nicht als self, sonder in Schleifen verarbeiten?
asteroid1 = 0
asteroid2 = 1
storage_abs = []
storage_rel = []


###################
### Before start
###################
#   Loading data
data = np.loadtxt("C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_SpoC_Mining/SpoC_Projekt/data/SpoC_Datensatz.txt")
for line in data:
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
    asteroids.append(p)                                                       # ACHTUNG, wirklich p schon anhängen?!?!?!
# asteroid_masses = data[:, -2]
# asteroid_materials = data[:, -1].astype(int)


##########################
### Essential functions
##########################
def asteroid_masse(self,i):
    """ Masse vom potentiellen Asteroiden abrufen
        Parameter:
            i:
                kann evtl. "self.asteroids[asteroid2]" sein!!        ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
        Rückgabe:   
            Masse von Asteroid i zwischen 0 und 1
    """
    return self.data[i, -2]

def asteroid_material(self,i):
    """ Material vom potentiellen Asteroiden abrufen (ist identisch zum Index, den wir benutzen wollen)
        Parameter:
            i:
                kann evtl. "self.asteroids[asteroid2]" sein!!       ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
        Rückgabe vom Material auf Asteroid i
    """
    return self.data[i, -1].astype(int)

def relative_material_stock(self):
    """ Bestand der bisher gesammelten Materialien (absolut und relativ) 
        Aufbau:
            Material 0-2:   storage_abs[0:2]
            Material 3:     storage_abs[3]      # = PROPELLANT
        Rückgabe:
            storage_rel:
                Vektor mit dem aktuellen, relativen(!) Bestand aller Materialien
    """
    storage_ges = np.sum(storage_abs)
    for i in range(0,storage_abs.index(storage_abs[-1])+1):
        storage_rel.append(np.round(storage_abs[i]/storage_ges,3))
    return storage_rel

def minimal_material(self):
    """ Gibt einem das Material wieder, welches bisher am wenigsten abgebaut wurde
        Rückgabe:
            STORAGE_min:
                Menge von Material mit absolutem Minimum
            storage_min:
                Menge von Material mit relativem Minimum
    """
    min_storage_abs = np.min(storage_abs)
    min_storage_rel = np.min(storage_rel)
    return min_storage_abs, min_storage_rel

def index_minimal_material():
    """ Gibt einem den Index des Materials, welches bisher am wenigsten abgebaut wurde
        Rückgabe:
            STORAGE_min:
                Index von Material mit absolutem Minimum
            storage_min:
                Index von Material mit relativem Minimum
    """
    min_storage_abs_ind = storage_abs.index(np.min(storage_abs))
    min_storage_rel_ind = storage_rel.index(np.min(storage_rel))
    return min_storage_abs_ind, min_storage_rel_ind

def tof(self):
    """ Berechnet die Flugzeit von Asteroid 1 zu Asteroid 2

        ACHTUNG: Sicherheit einbauen, dass t_arrival[-1] > t_spent[-2]!! Sonst ist tof negativ!
    """
    return (t_arrival[-1] - (t_arrival[-2] + t_spent[-2]))


def DV(self,variante,i,j):
    """ Berechnung von DV mit verschiedenen Varianten
        Args:
            Orbital
            Direct
            Indirect
            Lambert (default)
        i:  int
            aktueller Asteroid
        j:  int
            nächster Asteroid
    """

    if variante == "orbital":
        def DV_orbital(self):
            pass
    if variante == "direct":
        def DV_direct(self):
            pass
    if variante == "indirect":
        def DV_indirect(self):
            pass
    if variante == "lambert":
        def DV_lambert(self):
            
            # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution

            # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
            #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 

            r1, v1 = self.asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
            r2, v2 = self.asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
            
            l = pk.lambert_problem(r1=r1,r2=r2,tof=tof*pk.DAY2SEC, mu=self.MU, cw=False, max_revs=0)

            DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
            DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
            DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
            return DV                                        # ACHTUNG: Hier kommen Werte wie "622902.82..." raus !!

    else: DV_lambert()

    def propellant_used(self):
        self.propellant = self.propellant - DV / DV_per_propellant  # Und hier dann prop. -8..von 1 aus gerechnet
        

def DV_norm(self):
    """ Skalierung des DV """                                                                       # AUF WELCHEN BEREICH DENN SKALIERT???
    pass



# ACHTUNG: CLUSTERING, FUZZY UND ZEITOPTIMIERUNG HÄNGEN ALLE VONEINANDER AB!!!

def clustering_fuzzy(self):
    
    def clustering(self, i, eps, min_samples, metric, T):   #   Nach welchen Kriterien wird das Cluster gebildet? Ist man da flexibel?
        """ Festlegung des Clusters
            WICHTIG: Erstes Cluster ist ganz stark durch den verfügbaren propellant begrenzt
        """
        pass
        # cluster = pk.dbscan(asteroids)
        # return cluster.cluster(t_arrival[i], eps, min_samples, metric, T)

    def fuzzy(self): # Mathias
        """
            Erwartung:  Most valuable Asteroid (tank, rohstoff, masse)

            ==> Vorher Abfrage: Wenn Tank kleiner als Grenze (<3000), nur Ast mit Treibstoff betrachten
                    wie viele Ast. mit Kraftstoff sind noch im Cluster? Wenn weniger als beta, dann direkt in Tree-search 
                    (beta hoch, tank nach wechsel wird berücksichtigt)
        """
        f = 0                       # Das ist der Vorschlag von Fuzzy!
        return f

    j = fuzzy
    if j not in visited:        # j ist der vorgeschlagene Ziel-Asteroid
        visited.append(j)
    else: 
        self.sugg.pop(j)          # diesen Index aus den Vorschlägen löschen und fuzzy neu auswerten ohne j
        fuzzy()

def flugoptimierung(): # Sebastian
    """ Zeitoptimierung bezüglich:
            1. Zeitpunkt Abflug (früher aufbrechen?) --> davon ist Clustering enorm abhängig ==> ROHSTOFF GIBT DAS NICHT VOR (noch warten, wenn schon vollst. abgebaut)
            2. Flugdauer --> beeinflusst DV
        Sonstiges:
               Rohstoff-Minimum separat von propellant betrachten
    """
    pass



def abbau(self,i):
    """ Aktualisierung der vorhandenen Vektoren
    """
    def storage_update():
        """ Aktualisierung der Rohstoff-Vektoren, Unterschied zwischen Rohstoffen & propellant für den neuen Asteroiden aktualisiert!!!
        """
        mat_ind = self.asteroid_material(asteroid2) # Index vom Material
        # propellant
        if mat_ind == 3:
            propellant_found = np.minimum(asteroid_masse(mat_ind), (t_spent[-1]/TIME_TO_MINE_FULLY))
            propellant = np.minimum(1.0, propellant + propellant_found)
        # Restliche Rohstoffe
        self.storage_abs[mat_ind] += np.minimum(asteroid_masse(mat_ind), (t_spent[-1]/TIME_TO_MINE_FULLY))
        # propellant


    def time_update():
        """ Aktualisierung der Zeiten:
                1. Ankunft, days (!!)
                2. Abflug, days
                3. Abbau-Dauer, days --> (muss alles unter 60 liegen)
        """
        pass



def gütemaß():
    """ Wichtig als Vergleichsfaktor für die Auswertung!!
    """
    pass





###############################
### AUF GEHTS INS UNIVERSUM
###############################

class PSA_experiment():
    """ Ablauf der Reise in einer Schleife:
            1.  Clustering, dh. Datenbegrenzung
            2.  Flugoptimierung --> gibt tof und t_spent !!!
            3.  Vorschlag für einen optimalen nächsten Asteroiden mittels Fuzzy-Logik
            4.  Auswahl des 2. Asteroiden --> gibt den Index 
        Schleifenabbruchkriterien:
            1.  Keine Zeit mehr
            2.  Tank nicht mehr ausreichend für alle möglichen Asteroiden
            3.  Kein Tank mehr abbaubar
            4.  Alle Asteroiden besucht
            5.  Ein Rohstoff ausgeschöpft --> maximale Güte erreicht
        WICHTIG:
                Immer abfragen, ob das vorgegebene Zeitfenster noch eingehalten wird (Ankunftszeit - Abflugzeit <=! Zeitfenster)

    """

    def __init__(self, data) :
        self.data       =   data
        self.t_current  =   t_current
        self.t_current_e =  t_current_e
        self.t_left     =   t_left
        self.t_spent    =   t_spent 
        self.t_arrival  =   t_arrival
        self.propellant =   propellant
        self.asteroids  =   asteroids
        self.visited    =   visited
        self.sugg       =   sugg
        self.asteroid1  =   asteroid1
        self.asteroid2  =   asteroid2
        self.storage_abs =  storage_abs
        self.storage_rel =  storage_rel

    def journey(self):
        DV = []
        i = 0 # Start
        while i <= 5: #int(data[-1,0]+1): 
            self.asteroid1 = int(data[i,0])
            visited.append(self.asteroid1)

            # clustering_fuzzy.clustering(i, t_arrival[i], 800, 5,'orbital', 20)      # T wirklich auch 20? warum?
            i += 1
        
        return DV('lambert',1,2)
        print(visited)
        return visited


            # evtl. Flugoptimierung



    # def zeitplan(self):
    #     """ Erstellung vom Zeitplan
    #         Verwendete Größen:
    #             Arrival times:              double, days
    #                 Ankunftszeiten auf dem nächsten Planeten
    #             Mining/preparation time:    double, days
    #                 Dauer des Abbaus während Aufenthalt auf einem Planeten  --> ACHTUNG, nicht größer als 60
    #             Asteroids visited:          int
    #                 Indizes der besuchten Asteroiden
    #     """
    #     # import SpoC_Kontrolle as sp

    #     # x = sp.convert_to_chromosome([], True) #chromosome
    #     # return sp.pretty(x)

    #     def creating_x(self):
    #         x=[]
    #         return x
    #     # x.convert_to_chromosome()
    #     # x.pretty()
    #     # return x
    #     pass



experiment = PSA_experiment(data)
