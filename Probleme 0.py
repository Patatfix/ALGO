import random
Hmax = 10000

def compatible(creneau_1, creneau_2):
    if (creneau_1[0] >= creneau_2[0] and creneau_1[0] <= creneau_2[1]) or (creneau_1[1] >= creneau_2[0] and creneau_1[1] <= creneau_2[1]):
        return False
    return True

def crée_demandes(n,Hmax):
    demandes = []
    for i in range(n):
        hdeb = random.randint(0, Hmax)
        hfin = random.randint(hdeb, Hmax)
        while hfin == hdeb:
            hfin = random.randint(hdeb, Hmax)
        demandes.append((hdeb,hfin))
    return demandes

crée_demandes(10, Hmax)
