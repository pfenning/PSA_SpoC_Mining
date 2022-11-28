import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
from pykep import test

# pk.test.run_test_suite()

# Berechnung von Delta_V
# Bereits besuchte Asteoriden
# Verbleibende Zeit
# Übersicht über Materialien
# Ab- & Ankunftszeit (Lambert?)

'''
    Laufvariablen:
    -   Besuchte Asteoriden
    -   verbleibende Zeit
    -   gesammelte Materialien
    -   Vektoren für Abgabe (IDs, Ab- und Abflugzeitpunkte, usw.)
    
    Grundlagen:
    1.  Funktion: Berechnung Delta_V
    2.  Funktion: Abflug- & Ankunftszeitpunkt festlegen mit Lambert für neue Ebene
'''