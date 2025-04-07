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
    
    if isinstance(demandes[0], tuple) == True: # verifie si il y a déja l'indice de tri ou non
        demandes_classées = [[demandes[i], i] for i in range(n)] #si non, on ajoute un indice pour pouvoir ranger a la fin dans l'ordre original
    else : 
        demandes_classées = demandes #si oui
        
    if borne_de_tri == "début" : 
        demandes_classées = sorted(demandes_classées, key = lambda x: x[0][0]) #on trie par heure de début de rdv
    elif borne_de_tri == "fin": 
        demandes_classées = sorted(demandes_classées, key = lambda x: x[0][1]) #si on veut trier par heure de fin de rdv
    elif borne_de_tri == "longueur":
        demandes_classées = sorted(demandes_classées, key = lambda x: abs(x[0][0] - x[0][1])) #si on veut trier par durée du rdv
    else : 
        print("aucun tri effectué, borne_de_tri invalide")

    return (demandes_classées)



def optim_planning(demandes, opti = [], taille = 0):
    if len(demandes) == 0:
        return list(opti)
    new_demandes = demandes
    creneau_examiner = new_demandes.pop()
    solution1 = []
    if compatible_planning(opti,creneau_examiner):
        solution1 = optim_planning(demandes,opti+[creneau_examiner],taille+1)
    solution2 = optim_planning(demandes,opti,taille) 
    if len(solution1) > len(solution2):
        return solution1
    return solution2

# Tester avec des demandes aléatoires
Hmax = 10000
nombre_demandes = 20

# Générer des demandes aléatoires
demandes = crée_demandes(nombre_demandes, Hmax)

print("Demandes générées :")
for demande in demandes:
    print(demande)

# Appliquer l'optimisation
planification_optimale = optim_planning(demandes)
tri_rdv(planification_optimale)
print("\nPlanification optimale :")
for creneau in planification_optimale:
    print(creneau)

    
