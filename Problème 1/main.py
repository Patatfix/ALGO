import util
import numpy as np
import matplotlib.pyplot as plt
import time
import itertools


#%% Utilisable pour heuristiques locales

def inverser_arbres(tournee):
    """
    Amélioration locale par permutation de deux arbres dans la tournée.

    Cette méthode teste toutes les paires possibles d'arbres dans la tournée et les échange 
    si cela diminue la distance totale. Le processus est répété jusqu'à ce qu'aucune amélioration 
    ne soit trouvée.

    Complexité : O(n^2) par double itération

    Paramètre :
    - tournee : liste ou tableau numpy représentant l'ordre de passage par les arbres.

    Return :
    - Une tournée améliorée, avec éventuellement une distance totale plus courte.
    """
    tournee = tournee.copy()  # On copie pour éviter de modifier l'entrée
    distance_totale = util.distance_totale(tournee)
    amelioration = True

    while amelioration:
        amelioration = False
        for i in range(len(tournee)):
            for j in range(i + 1, len(tournee)):
                tournee_bis = tournee.copy()
                # Échange de deux arbres
                tournee_bis[[i, j]] = tournee_bis[[j, i]]
                nouvelle_distance = util.distance_totale(tournee_bis)
                if nouvelle_distance < distance_totale:
                    tournee = tournee_bis
                    distance_totale = nouvelle_distance
                    amelioration = True
    # print(tournee)
    return tournee

def inverse_arete(tournee):
    """
    objectif : améliore la tournée en inversant 2 segments (arêtes).

    Cette méthode parcourt les paires de positions non adjacentes dans la tournée et 
    inverse le segment entre elles si cela réduit la distance totale. Le processus est 
    répété tant qu'une amélioration est trouvée.

    Complexité : O(n^2) par double boucle d'itération.

    Paramètre :
    - tournee : tableau numpy représentant l’ordre de visite des arbres.

    Retour :
    - Une tournée améliorée avec une distance totale réduite si possible.
    """
    tournee = np.copy(tournee)
    n = len(tournee)
    amelioration = True

    while amelioration:
        amelioration = False
        for i in range(1, n - 2):
            for j in range(i + 1, n):
                if j - i == 1:  # On évite d'inverser deux éléments consécutifs
                    continue
                # Inversion du segment entre i et j
                nouvelle_tournee = np.concatenate((
                    tournee[:i],
                    tournee[i:j][::-1],
                    tournee[j:]
                ))
                if util.distance_totale(nouvelle_tournee) < util.distance_totale(tournee):
                    tournee = nouvelle_tournee
                    amelioration = True
                    break
            if amelioration:
                break

    return tournee

def plus_court_chemin_exhaustif(points):
    # On extrait les points intermédiaires (sans départ ni arrivée)
    n = len(points)
    points_intermediaires = [p for p in points[1: n-1]]

    min_dist = float('inf')
    meilleur_chemin = []
    
    # Si points est déjà optimal 
    # (En génral ce n'est pas le cas car on envoie des troncons de la bonne taille)
    # (Sauf pour le dernier tronçon)
    if np.shape(points)[0] <= 3:
        return points
    
    # On itére sur toutes les permutations possibles des points intermédiaires :
    # On les testes toutes et on garde la meilleure
    for perm in itertools.permutations(np.array(points_intermediaires)):
        chemin = np.concatenate(([points[0]], np.array(perm), [points[n-1]]))
        d = util.distance_totale(chemin)
        
        # Si le chemin est meilleur alors on le garde
        if d < min_dist:
            min_dist = d
            meilleur_chemin = chemin
    
    return meilleur_chemin






#%% Methode exhaustif 

def calcul_tournee_exhaustif(arbres, chemin=[[0, 0]]):

    # Initialisation des variables
    distance_opti = float('inf') # Distance optimale infinie pour être sûr qu'elle soit toujours minorée
    chemin_opti = []
    n = len(arbres)
    distance_chemin = 0

    # Appel de la fonction auxiliaire avec les variables initiales
    chemin_opti, distance_opti = aux_calcul_tournee_exhaustif(chemin, 0, distance_chemin, arbres, chemin_opti, distance_opti, n)

    return chemin_opti # Renvoi le chemin optimal d'après le parcours exhaustif


def aux_calcul_tournee_exhaustif(chemin, taille_chemin, distance_chemin, arbres_restants, chemin_opti, distance_opti, n):

    # Cas de base n°1 : la distance parcourue par le chemin dépasse la distance optimale locale
    if distance_chemin > distance_opti:
        return chemin_opti, distance_opti # Le chemin n'est dès lors pas le chemin plus optimal

    # Cas de base n°2 : le chemin est terminé
    if taille_chemin == n:
        distance_chemin_total = distance_chemin + util.distance(chemin[-1], (0, 0)) # Rajoute la distance pour revenir à l'entrée
        if distance_chemin_total < distance_opti:
            return np.vstack((chemin, [0, 0])), distance_chemin_total # Empilement vertical : ajoute le point (0,0) à la fin du chemin.
                                                                      # Ce chemin est le nouveau chemin optimal
        return chemin_opti, distance_opti # Sinon, le chemin optimal ne change pas

    # Cas général :
    for i in range(len(arbres_restants)):
        arbre = arbres_restants[i]
        dist = distance_chemin + util.distance(chemin[-1], arbre)  # Nouvelle distance après ajout du point
        arbres_restants_bis = np.delete(arbres_restants, i, axis=0) # Mise à jour du nombre d'arbres restant

        # Appel récursif sur le nouveau chemin (avec le nouvel arbre)
        chemin_opti, distance_opti = aux_calcul_tournee_exhaustif(np.vstack((chemin, arbre)), taille_chemin + 1, dist,
                                                                  arbres_restants_bis, chemin_opti, distance_opti, n)

    return chemin_opti, distance_opti # Renvoi le chemin le plus optimal jusqu'ici


#%% Methode glouton

def parcours_glouton(coords, coord_init = (0,0)):
    """
    Args:
        coords: tableau numpy, liste des points (n, 2)
        coord_init: tuple (x, y), point initial
    Returns:
        Liste des coordonnées ordonnées selon l'ordre glouton
    """
    new_coord = np.zeros((1,2))
    new_coord[0,0] = coord_init[0]
    new_coord[0,1] = coord_init[1]
    for _ in range(len(coords)):
        index_min = 0
        distance_min = util.distance(coords[0,:],new_coord[-1,:])
        for j in range(1,len(coords)):
            curr_dist = util.distance(coords[j][:],new_coord[-1,:])
            if curr_dist <= distance_min:
                index_min = j
                distance_min = curr_dist
        new_coord = np.concatenate((new_coord, coords[index_min:index_min+1]), axis=0)
        coords = np.delete(coords, index_min, axis=0)
    return new_coord



#%% Methode glouton+heuristique



def parcours_glouton2(coords,alpha, coord_init = (0,0)):
    """
    Args:
        coords: tableau numpy, liste des points (n, 2)
        coord_init: tuple (x, y), point initial
    Returns:
        Liste des coordonnées ordonnées selon l'ordre glouton
    """
    new_coord = np.zeros((1,2))
    new_coord[0,0] = coord_init[0]
    new_coord[0,1] = coord_init[1]
    while len(coords) > 0:
        index_min = 0
        liste_index_mins = [0]  # Liste des indices proches
        distance_min = util.distance(coords[0, :], new_coord[-1, :])

        for i in range(1, len(coords)):
            curr_dist = util.distance(coords[i, :], new_coord[-1, :])
            if curr_dist <= distance_min:
                index_min = i
                distance_min = curr_dist
                # Vérifie et modifie `liste_index_mins`
                for j in reversed(liste_index_mins):
                    if util.distance(coords[index_min, :], coords[j, :]) > distance_min*alpha:
                        liste_index_mins.remove(j)
                if index_min not in liste_index_mins:
                    liste_index_mins.append(index_min)
                
        # Applique un exaustif locale
        select_coords = coords[liste_index_mins]
        deb = np.array([[new_coord[-1,0],new_coord[-1,1]]])
        select_coords = np.concatenate((deb,select_coords),axis=0)
        new_coord_local = plus_court_chemin_exhaustif(select_coords)
        
        # Concaténe la sous-tournée avec le chemin global
        new_coord = np.concatenate((new_coord, new_coord_local), axis=0)
        
        # Supprime les points traités
        for j in reversed(liste_index_mins):
            coords = np.delete(coords, j, axis=0)

    return new_coord

"""compléxité n^3 + n*m! avec m<<n, tous du alpha qu'on prends
dans le pire des cas n*n!"""




# %% Pondération


def ponderation(coords, i, lis_i, r=50):
    """ 
    On sélectionne le point suivant en fonction de sa distance et du nombre de points qui l'entoure
    """
    n = len(coords)
    distances = np.zeros(n)
    W = np.zeros(n)
    for k in range(n):
        # On calcule la distance pour chaque point différent de celui où on est
        d = util.distance(coords[i], coords[k])
        
        # Si on la déjà parcouru on a une distance infinie
        if k in lis_i +[i]:
            distances[k] = float('inf')
        if k != i and k not in lis_i:
            d = util.distance(coords[i], coords[k])

            distances[k] = d
    
        w = 0
        for j in range(n):
            # Si on est dans le cercle de rayon r alors on pondere
            if util.distance(coords[k], coords[j]) <= r:
                # 5 est une valeur arbitraire > 1
                w += 5
        W[k] += w
    pondere = distances * W
    # On renvoie le minimum de la distance pondérée
    return np.argmin(pondere)


def evaluation(coords):
    # On ajoute le point [(0, 0)] à coords s'il n'est pas dedans
    if (0, 0) not in coords:
        coords = [(0, 0)] + coords
    n = len(coords)
    i = np.random.randint(0, n)
    lis_i = [i]
    chemin = [coords[i]]
    for k in range(n-1):
        # On prend le "meilleur point" déterminer par la pondération
        i = ponderation(coords, i, lis_i)
        # On veut pas repasser deux fois par le même points
        lis_i.append(i)
        chemin.append(coords[i])
    return np.array(chemin)


def heuristique_locale(coords, q=9):
    # Si le set de coordonnées est assez petit en renvoie directement la version exhaustive
    if len(coords) <= 7:
        return calcul_tournee_exhaustif(coords), 0
    
    # Sinon on approche la solution optimale avec evaluation que l'on améliorera ensuite
    chemin = evaluation(coords)
    dc = util.distance_totale(chemin) # Distance initiale, sans heuristique
    n = len(chemin)
    for i in range(n//q):
        if i == n//q: # Le cas où la liste n'est pas d'une taille divisible par q
            c = chemin[i*q:]
            
            # que l'on optimise avec l'heuristique en gardant toujours le même début et la même fin
            pcce = plus_court_chemin_exhaustif(c)
            
            # On remplace par la version améliorée...
            chemin[i*q:] = pcce
        else:
            # On découpe notre chemin en tronçons, de taille q
            c = chemin[i*q: (i+1) * q]
            
            # que l'on optimise avec l'heuristique en gardant toujours le même début et la même fin
            pcce = plus_court_chemin_exhaustif(c)
            
            # On remplace par la version améliorée...
            chemin[i*q: (i+1) * q] = pcce

    diff = round(dc - util.distance_totale(chemin), 3) # Distance après heuristique
    # diff permet de mesurer l'utilité de notre heuristique...
    return chemin, diff



#%% 

def test_evaluation(N=100, nomfichier="exemple2.txt"):
    dmin = float('inf')
    moy_diff = 0
    lis_diff = []
    t_min = []
    
    for i in range(N):
        if i % (N/10) == 0:
            print("###   ", i, "   ####")
        start = time.time()
        
        coords = util.lire_fichier_coords(nomfichier)
        tournee, diff= heuristique_locale(coords)
        d =  round(util.distance_totale(tournee), 3) # On arrondit pour pas avoir trop de chiffres décimaux
        
        moy_diff += diff
        lis_diff.append(diff)
        if d < dmin:
            t_min = tournee
            dmin = d
        end = time.time()

        print(d)
        print("Temps d'exécution :", round(end - start, 2), "secondes")
        print()
        
    
    
    print("#################################", "\n")
    print(dmin, "\n")
    print()
    print(moy_diff/N)
    print()
    print("#################################")
    
    util.affiche_tournee(t_min)
    util.histo(lis_diff)
    return

#test_evaluation(100, "exemple2.txt")

# %% Methode dichotomique

def distance4(c1, c2):
    # On cherche à déterminer le meilleure recollage entre deux chemins...
    d = {(0, 0): util.distance(c1[0], c2[0]), (-1, 0): util.distance(c1[-1], c2[0]), (0,-1): util.distance(c1[0], c2[-1]), (-1, -1): util.distance(c1[-1], c2[-1])}
    return min(d, key = d.get)


def dicho(coords, x=False):
    n = len(coords)
    if n <= 2:
        # Cas de base: Si le chemin est trop petit alors on le renvoie
        return coords
    if not x:
        # On divise selon l'axe x
        sort_coords = sorted(coords, key=lambda x: x[0])
    else:
        # On divise selon l'axe y
        sort_coords = sorted(coords, key=lambda x: x[1])
    # On prend les deux moitiées
    coords_1 = sort_coords[:n//2]
    coords_2 = sort_coords[n//2:]
    
    # Sur lesquels on ré-exécute notre fonction
    c_d = dicho(coords_1, not x)
    c_g = dicho(coords_2, not x)
    
    # Puis on prend le meilleur recollage
    k = distance4(c_d, c_g)
    if k[0] == -1 and k[1] == 0:
        return c_d + c_g
    if k[0] == -1 and k[1] == -1:
        return c_d + c_g[::-1]
    if k[0] == 0 and k[1] == -1:
        return c_d[::-1] + c_g[::-1]
    if k[0] == 0 and k[1] == 0:
        return c_d[::-1] + c_g





#%% Fonctions voisin


"""
Ici on a codé différentes fonctions voisins, qui prennent chacune en argument un parcours
déjà crée et renvoie un autre parcours "voisin", c'est à dire modifié partiellement de manière
aléatoire. Le choix de la fonction voisin a donc un impact sur l'efficacité et le temps
d'exécution du recuit simulé. 
"""

def voisin1(tournée,taille_max=60):                  #voisin1 crée une copie d'un parcours
    taille = np.random.randint(2,taille_max)         #donné en argument et échange deux points
    i = np.random.randint(0,len(tournée)-taille)     #de manière aléatoire (séparés par (taille_max-2) points au maximum)
    
    copie = tournée.copy()
    
    t = copie[i:i+taille,:]
    #print(t)
    inter = t[0,:].copy()
    t[0,:]=t[-1,:].copy()
    t[-1,:]=inter
    #print(t)
    return copie
#voisin(glouton)

def voisin2(tournée,taille_max=50,seuil = 670):             #voisin 2 crée une copie d'un parcours
    if util.distance_totale(tournée)<seuil:          #donné en argument et inverse une séquence du parcours
        taille = np.random.randint(2,30)        #choisie aléatoirement, de taille maximale taille_max
    else:
        taille = np.random.randint(2,taille_max)
    i = np.random.randint(0,len(tournée))
    copie = tournée.copy()
    t = copie[i:i+taille,:]
    
    l=[]
    n = len(t)
    for a in range(1,n+1):
        l.append(t[-a,:])
    t[:]=np.reshape(l,(n,2))
    
    return copie

def voisin3(tournée,seuil=670):                           #voisin 3 crée une copie d'un parcours
    if util.distance_totale(tournée)<seuil:        #donné en argument pour chaque couple de points
        taille = np.random.randint(2,30)        #les échanges avec une probabilité de 0.5
    n = len(tournée)
    
    copie = tournée.copy()
    for i in range(0,n,2):
        
        r = np.random.uniform(0,1)
        if r < 0.5:
            
            t = copie[i:i+2,:]
            #print(t)
            
            inter = t[0,:].copy()
            t[0,:]=t[-1,:].copy()
            t[-1,:]=inter
        
    return copie


    
#%% Fonctions de température

def f1(b,nb_iter,T0):                              #Diminue de manière constante mais reste à valeurs importantes
    return T0 - T0*(1-np.exp((-b)/nb_iter))


def f2(b,nb_iter,T0):
    return T0 * (nb_iter-b)/nb_iter                         #Diminue de manière constante

def f3(b,nb_iter,T0):                                        #Diminue fort puis lentement
    return T0 * 1/(np.log(b+2))*(nb_iter-b)/nb_iter

def f4(b,nb_iter,T0):                              #Diminue de manière constante mais reste à valeurs importantes
    return T0 - T0*(1-np.exp((-b)/(0.5*nb_iter)))

    
"""
Plus la température est grande, plus l'algorithme accepte des solutions de plus grandes énergies,
donc la fonction température à un réel impact sur la convergence vers une bonne solution
"""



    
#%% Algorithme de recuit simulé

sol = []
dist_sol = float('inf')                
def recuit_simulé(tournée,voisin,nb_iter,T0,f):
    global sol, dist_sol
    sol = []
    dist_sol = float('inf')                   #on initialise dist_sol a +infini pour
                                            #que la première solution prennent forcement la place
                                            #de sol
    for b in range (nb_iter):
        dist = util.distance_totale(tournée)    #on évalue la longueur du parcours actuel
        
        v = voisin(tournée)                    #on crée un nouveau parcours voisin
        
        E = util.distance_totale(v)            #on évalue la longueur du nouveau parcours
        T =  f(b,nb_iter,T0)                   #On actualise la température
                
        if E < dist:                          #si la solution est meilleure, on la choisit
        
            tournée[:]=v[:]
        if E < dist_sol:              #si elle est moins bien, on la choisis ou non selon la probabilité p 
            sol[:]=v.copy()
            dist_sol = E
        else:
            r = np.random.uniform(0,1)
            p = np.exp((dist-E)/T)
            #print(p)
            if r < p:
                tournée[:]=v[:]

        if b%100==0:               #tout les 100 itérations, on affiche l'évaluation de la solution actuelle
            print(f'Distance {b} = {util.distance_totale(tournée)}')
    print(f'distance finale = {util.distance_totale(sol)}')
    return np.array(sol)



#%% Recuit puis inverse_arete

def recuit_puis_inverse_arete(tournée,nb_iter=50000,T0=3,T=f4,voisin=voisin2):
    s1 = recuit_simulé(tournée, voisin, nb_iter, T0,T)
    s2 = inverse_arete(s1)
    return s2


#%% Inverse 3 arêtes

def inverser_3_arete(tournee):
    """
    Amélioration du inverser_arete : tente d'améliorer la tournée en inversant/permutant jusqu'à trois arêtes simultanément.

    Cette fonction explore différentes permutations de trois segments consécutifs dans la tournée afin de trouver 
    une configuration qui réduit la distance totale du parcours. Elle essaie plusieurs combinaisons de réordonnancement 
    de ces trois segments. 

    Complexité : O(n^3), ce qui rend la fonction coûteuse pour de grandes tournées. 
    C'est pour cette raison qu'elle est mentionnée comme non utilisée.

    Paramètre :
    - tournee : tableau numpy représentant une séquence d'indices des points à visiter (les arbres)

    Retour :
    - Une version possiblement améliorée de la tournée (ordre des visites) avec une distance totale plus faible.
    """
    tournee = np.copy(tournee)  # On travaille sur une copie pour ne pas modifier la tournée d'origine
    n = len(tournee)
    amelioration = True

    # On boucle tant qu'une amélioration est trouvée
    while amelioration:
        amelioration = False
        # Choix de la premiere arete, en laissant de la place pour les 2 autres aretes d'ou le n-5
        for i in range(n - 5):
            # Choix de la  deuxième arete, au moins 1 positions après l'arete (i, i+1), donc 2 apres i
            for j in range(i + 2, n - 3):
                # Choix de la troisième arete, au moins 1 positions après l'arete (j, j+1), donc 2 apres j
                for k in range(j + 2, n - 1):
                    # Découpage de la tournée en 4 segments A-B-C-D
                    A = tournee[:i+1]
                    B = tournee[i+1:j+1]
                    C = tournee[j+1:k+1]
                    D = tournee[k+1:]

                    # Liste de permutations possibles des segments B et C
                    configurations = [
                        np.concatenate((A, B[::-1], C, D)),      # Inverser B
                        np.concatenate((A, B, C[::-1], D)),      # Inverser C
                        np.concatenate((A, B[::-1], C[::-1], D)),# Inverser B et C
                        np.concatenate((A, C, B, D)),            # Echanger B et C
                        np.concatenate((A, C[::-1], B, D)),      # Echanger B et C, inverser C
                        np.concatenate((A, C, B[::-1], D)),      # Echanger B et C, inverser B
                        np.concatenate((A, C[::-1], B[::-1], D)) # Echanger et inverser B et C
                    ]

                    # Calcul de la distance de la tournée actuelle
                    best_distance = util.distance_totale(tournee)

                    # Parcours de toutes les configurations et mise à jour si on trouve mieux
                    for config in configurations:
                        d = util.distance_totale(config)
                        if d < best_distance:
                            tournee = config
                            amelioration = True
                            break  # Sortie de la boucle si amélioration trouvée
                    if amelioration:
                        break
                if amelioration:
                    break
            if amelioration:
                break

    return tournee


#%%Annexe pour les tests et affichages

def test_evaluation(N=100, nomfichier="exemple2.txt"):
    # On exécute juste N itérations de la fonction évaluation pour obtenir une
    # solution proche de l'optimale (résultat dépendant du point de départ aléatoire)
    
    # On garde la meilleure solution
    dmin = float('inf')
    moy_diff = 0
    lis_diff = []
    t_min = []
    
    for i in range(N):
        if i % (N/10) == 0:
            print("###   ", i, "   ####")
        start = time.time()
        
        coords = util.lire_fichier_coords(nomfichier)
        tournee, diff= heuristique_locale(coords)
        d =  round(util.distance_totale(tournee), 3) # On arrondit pour pas avoir trop de chiffres décimaux
        
        moy_diff += diff
        lis_diff.append(diff)
        if d < dmin:
            t_min = tournee
            dmin = d
        end = time.time()

        print(d)
        print("Temps d'exécution :", round(end - start, 2), "secondes")
        print()
        
    
    
    print("#################################", "\n")
    print(dmin, "\n")
    print()
    print(moy_diff/N)
    print()
    print("#################################")
    
    util.affiche_tournee(t_min)

    # On affiche un histogramme de l'utilité de l'heursitique locale sur ce problème
    util.histo(lis_diff)
    return

def creer_donnees(n, xmin=-30, xmax=30):
    """
    Génère rapidement n points 2D dans un carré [xmin, xmax] x [xmin, xmax]
    """
    x = np.random.uniform(xmin, xmax, n)
    y = np.random.uniform(xmin, xmax, n)
    return np.column_stack((x, y))  # Renvoie un array (n, 2)

def afficher_donnees(données):
    plt.scatter(données[:,0], données[:,1], c='green')
    plt.show()

def affiche_temperature(f,T0):
    x = np.linspace(0, 100, 50)
    y = f(x,100,T0)
    plt.scatter(x, y, c='red')
    plt.plot()

def compare_temperature(f1,f2,f3,f4,T0):
    x = np.linspace(0, 100, 50)
    y1 = f1(x,100,T0)
    y2 = f2(x,100,T0)
    y3 = f3(x,100,T0)
    y4 = f4(x,100,T0)
    plt.plot(x, y1, c='red', label='f1')
    plt.plot(x, y2, c='blue',label='f2')
    plt.plot(x, y3, c='green',label='f3')
    plt.plot(x, y4, c='black',label='f4')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("T(x)")
    plt.grid(True)
    plt.title('Visualisation des différentes fonctions de températures')
    plt.show()


def test_recuit(donnees,nb_iter=50000,T0=2.5,T=f4,voisin=voisin2):
    s0 = evaluation(donnees)
    start = time.time()
    s1 = recuit_puis_inverse_arete(s0,nb_iter,T0,T,voisin)
    s = heuristique_locale(s1)
    print(util.distance_totale(s))
    util.affiche_tournee(s)

    end = time.time()
    print(f"Temps d'exécution : {end-start}")