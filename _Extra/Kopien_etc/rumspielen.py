import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
# from pykep import dbscan

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

t_arrival = [0,62.34]
t_spent = [50.1,12.2] # prepping material

propellant = 1.0
asteroids = []
visited = []
sugg = []                   # hier nicht addieren, immer neu löschen...dann nicht als self, sonder in Schleifen verarbeiten?
asteroid1 = 345
asteroid2 = 654
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
asteroid_masses = data[:, -2]
asteroid_materials = data[:, -1].astype(int)

data_fuel = []
asteroids_fuel = []
i = 0
while i < len(data):
    if data[i,-1].astype(int) == 3:
        data_fuel.append(data[i])
        i += 1
    else: i += 1
for line in data_fuel:
    p = pk.planet.keplerian(T_START,(line[1],line[2],line[3],line[4],line[5],line[6],),
        MU_TRAPPIST,
        G * line[7],  # mass in planet is not used in UDP, instead separate array below
        1,  # these variable are not relevant for this problem
        1.1,  # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0])),
    )
    asteroids_fuel.append(p)                                                       # ACHTUNG, wirklich p schon anhängen?!?!?!
asteroid_masses = data[:, -2]
asteroid_materials = data[:, -1].astype(int)





# class rumspielen:
#       STORAGE= [10,2,4,6]
#     # def __init__(self):
#     #     #self.vektor = vektor
#     #     pass     
#     def calc_minimum(vektor):
#         return(
#         STORAGE.index(np.min(vektor))
#         )
# print(rumspielen.calc_minimum(STORAGE))

# storage = []
# storage_ges = np.sum(STORAGE)
# for i in range(0,STORAGE.index(STORAGE[-1])+1):
#     storage.append(np.round(STORAGE[i]/storage_ges,3))
# print(STORAGE[1]/storage_ges)
# print(storage)


# Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution
# DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
# tof = t_arrival[-1] - t_arrival[-2] - t_spent[-2]
# r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
# r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])         
# l = pk.lambert_problem(r1=r1,r2=r2,tof=tof*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0)
# DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
# DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
# DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)
# print(propellant - (DV / DV_per_propellant))



# def asteroid_material(i):
#     """ Material vom potentiellen Asteroiden abrufen (ist identisch zum Index, den wir benutzen wollen)
#         Parameter:
#             i:
#                 kann evtl. "self.asteroids[asteroid2]" sein!!       ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
#         Rückgabe vom Material auf Asteroid i
#     """
#     i = asteroid2
#     return data[i, -1].astype(int)
# def asteroid_masse(i):
#     """ Masse vom potentiellen Asteroiden abrufen
#         Parameter:
#             i:
#                 kann evtl. "self.asteroids[asteroid2]" sein!!        ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
#         Rückgabe:   
#             Masse von Asteroid i zwischen 0 und 1
#     """
#     return data[i, -2]
# mat_ind = asteroid_material(asteroid2)
# print(asteroid_masse(mat_ind), np.minimum(asteroid_masse(mat_ind), (t_spent[-1]/TIME_TO_MINE_FULLY)))





    #################################
    ### SCHRITT 1:      Clustering      UNEINGESCHRÄNKT
    #################################
    # # Annahme:  Wir befinden uns auf einem Asteroiden
    # from pykep import phasing
    # knn = phasing.knn(asteroids, ERG_t_arr[-1], 'orbital', T = 30) #                                            ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
    # radius = 1500
    # neighb, neighb_ids = psa.clustering(knn, var, radius)
    # # print(len(neighb_ids))
    # # print("Nachbarn: ", neighb_ids)
    # i = 0
    # dv_min_2 = []
    # while i < len(neighb_ids):
    #     if neighb_ids[i] not in visited_ind:
    #         asteroid2_id = neighb_ids[i]
    #         asteroid2 = asteroids[asteroid2_id]
    #         t_m_opt, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(asteroid1, asteroid2, ERG_t_arr[-1] + t_opt, t_opt)
    #         dv_min_2.append(dv_min_)
    #         i += 1
    #     else:
    #         i += 1

    # dv_min_2_intermediate_INDEX = dv_min_2.index(min(dv_min_2))
    # asteroid2_id = neighb_ids[dv_min_2_intermediate_INDEX]
    # asteroid2 = asteroids[asteroid2_id]

    # # Asteroiden aus Liste streichen
    # asteroids = np.delete(asteroids, asteroid2_id)
    # visited_ind.append(asteroid2_id)  
    # print("Besuchte Asteroiden: ", visited_ind)

    # # ACHTUNG: WENN CLUSTER DURCH BEDINGUNG LEER, DANN IST "dv_min_2" LEER UND ER BESUCHT DEN GLEICHEN ASTEROIDEN NOCHMAL!!! 
    # # DAS IST ZU VERMEIDEN!!!!!!

# DV Rumspielerei
# def get_DV(asteroid1, asteroid2, t_start, t_flug, print_result=False):  #variante="lambert", 
#     """ Berechnung von DV mit verschiedenen Varianten
#         Args:
#             Orbital
#             Direct
#             Indirect
#             Lambert (default)
#         i:  int
#             aktueller Asteroid
#         j:  int
#             nächster Asteroid
#     """
#     # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution
#     # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
#     #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 
#     # r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
#     #t_start_rv1 = T_START.mjd2000 + t_start
#     r1, v1 = asteroid1.eph(T_START.mjd2000 + t_start)    
#     # r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
#     r2, v2 = asteroid2.eph(T_START.mjd2000 + t_start + t_flug)            
#     l = pk.lambert_problem(r1=r1,r2=r2,tof=t_flug*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0
#     DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
#     DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
#     DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
#     return DV   

#     if variante == "orbital":
#         def DV_orbital():
#             pass
#     if variante == "direct":
#         def DV_direct():
#             pass
#     if variante == "indirect":
#         def DV_indirect():
#             pass
#     if variante == "lambert":
#         def DV_lambert():            
#             # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution
#             # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
#             #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 
#             # r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
#             r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_start)
#             # r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
#             r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_start + t_flug)            
#             l = pk.lambert_problem(r1=r1,r2=r2,tof=tof*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0)
#             DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
#             DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
#             DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
#             return DV                                        # ACHTUNG: Hier kommen Werte wie "622902.82..." raus !!
#     # else: DV_lambert()
#     # def propellant_used():
#     #     propellant = propellant - get_DV / DV_per_propellant  # Und hier dann prop. -8..von 1 aus gerechnet
# # print(T_START.mjd2000)







# DV berechnen
import PSA_functions as psa
# 1) Spoc-Kontrolle
# Also break if the time of flight is too short (avoids singular lambert solutions)
ast_1_idx = 9953
ast_1_kp = asteroids[ast_1_idx]
ast_2_idx = 6961
ast_2_kp = asteroids[ast_2_idx]

t_opt = 0
t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize(ast_1_kp, ast_2_kp, 0 + t_opt, t_opt,,,
                                         time_at_arrival = [t_abflug_opt_ + t_flug_min_dv_]
time_spent_preparing = [t_abflug_opt_]
tof = t_flug_min_dv_

# Compute the ephemeris of the asteroid we are departing
r1, v1 = asteroids[ast_1_idx].eph(
    T_START.mjd2000 + time_at_arrival[i - 1] + time_spent_preparing[i - 1]
)

# Compute the ephemeris of the next target asteroid
r2, v2 = asteroids[ast_2_idx].eph(
    T_START.mjd2000 + time_at_arrival[i]
)

# Solve the lambert problem for this flight
l = pk.lambert_problem(
    r1=r1, r2=r2, tof=tof * pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0
)

# Compute the delta-v necessary to go there and match its velocity
DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)

# Compute propellant used for this transfer and update ship propellant level
propellant = propellant - DV / DV_per_propellant

print("DV Spoc Kontrolle: ", DV)