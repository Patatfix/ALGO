import random
Hmax = 10000


def compatible(creneau_1, creneau_2): # Vérifie que deux créneaux sont compatible ensemble
    if (creneau_1[0] >= creneau_2[0] and creneau_1[0] <= creneau_2[1]) or (creneau_1[1] >= creneau_2[0] and creneau_1[1] <= creneau_2[1]):
        return False
    return True


def compatible_planning(planning, creneau): # 
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



def tri_rdv(demandes, borne_de_tri = "début"): #trie les rdv par ordre d'heure de début et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
        
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
    

demandes = crée_demandes(10, Hmax)
demande_classee = tri_rdv(demandes)
    
total = []

# Marche pas encore
def solution_exhaustive(demandes, curr = [], i=0,d=0): # Énumération exhaustive appris en mineure info
    maxi = 0
    meilleur_planning = []
    if i == len(demandes):
        total.append(curr)
        if d == len(demandes)-1:
            for planning in total:
             taille = len(planning)
             if taille >= maxi:
                 maxi = taille 
                 meilleur_planning = planning
        d += 1
        i = d
        curr = []
    print(f"d : {d}")
    print(f"i : {i}")
    if compatible_planning(curr, demandes[i-1]):    
        solution_exhaustive(demandes, curr, i+1, d)
        curr.append(demandes[i])
        solution_exhaustive(demandes, i+1, d)
        curr.pop()
    return

print(solution_exhaustive(demande_classee))



    
