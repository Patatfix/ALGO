import random
Hmax = 10000

def compatible(creneau_1, creneau_2):
    return creneau_1[1] < creneau_2[0] or creneau_2[1] < creneau_1[0]


def compatible_planning(planning, creneau):
    for cre in planning:
        if not compatible(cre, creneau):
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

def tri_rdv(demandes, borne_de_tri = "début"): #trie les rdv par ordre d'heure de début et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
    #bornes_de_tri peut etre "début", "fin" ou "longueur"
    n = len(demandes)

    if borne_de_tri == "début" : 
        demandes_classées = sorted(demandes, key = lambda x: x[0]) #on trie par heure de début de rdv
    elif borne_de_tri == "fin": 
        demandes_classées = sorted(demandes, key = lambda x: x[1]) #si on veut trier par heure de fin de rdv
    elif borne_de_tri == "longueur croissante":
        demandes_classées = sorted(demandes, key = lambda x: abs(x[0] - x[1])) #si on veut trier par durée du rdv croissante
    elif borne_de_tri == "longueur décroissante":
        demandes_classées = sorted(demandes, key = lambda x: abs(x[0] - x[1])) #si on veut trier par durée du rdv decroissante
        demandes_classées.reverse()
    else : 
        print("aucun tri effectué, borne_de_tri invalide")

    return (demandes_classées)


def optim_planningv1(demandes):
    #demandes = supprime_longs(demandes)
    demandes = tri_rdv(demandes, "fin")
    n = len(demandes)

    planning = []
    planning.append(demandes[0])

    i=1
    while i < n:

        if demandes[i][0] >= planning[-1][1]:
            planning.append(demandes[i])

        i += 1

    return planning

"""
demandes = crée_demandes(10, Hmax)
demandes_classées = tri_rdv(demandes, borne_de_tri = "fin")


print(demandes_classées, "\n")
print(optim_planningv1(demandes))
"""


def optim_planningv2(demandes, opti = [], taille = 0):
    if len(demandes) == 0:
        return list(opti)
    new_demandes = demandes
    creneau_examiner = new_demandes.pop()
    solution1 = []
    if compatible_planning(opti,creneau_examiner):
        solution1 = optim_planningv2(demandes,opti+[creneau_examiner],taille+1)
    solution2 = optim_planningv2(demandes,opti,taille) 
    if len(solution1) > len(solution2):
        return solution1
    return solution2

# Tester avec des demandes aléatoires
Hmax = 10000
nombre_demandes = 20


# Générer des demandes aléatoires
#demandes = crée_demandes(nombre_demandes, Hmax)
demandes = [(0,1),(2,5),(5,8),(2,4),(3,4),(5,9),(1,2)]


print("Demandes générées :")
for demande in demandes:
    print(demande)

# Appliquer l'optimisation
planification_optimale = optim_planningv2(demandes)
planification_optimal = tri_rdv(planification_optimale)
print("\nPlanification optimale :")
for creneau in planification_optimal:
    print(creneau)

    
