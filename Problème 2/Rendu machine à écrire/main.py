import numpy as np #pour les calculs de cout
import time #pour les temps d'execution
import matplotlib.pyplot as plt #pour les graphiques de temps d'execution
import sys #pour modifier les limites du logiciels concernant le nombre de recursion max
sys.setrecursionlimit(1000000)

def lire_fichier(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            texte = f.read().strip()  # Supprime les espaces et retours à la ligne inutiles
            mots = texte.split()  # split() sans argument gère les espaces multiples proprement
        return mots
    except FileNotFoundError:
        raise ValueError("Le fichier spécifié est introuvable.")
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier : {e}")


def enregistrer_fichier_texte(texte_opti, nom_fichier): #enregistre un texte sous forme de liste de ligne et l'enregistre avec le nom donné
    fichier = open(nom_fichier, "a")
    for ligne in texte_opti:
        fichier.write(str(ligne) + "\n")
    fichier.close()
    return


def liste_taille_fichier(nom_fichier): #prend un fichier et renvoie une listes des tailles des mots
    liste_mots = lire_fichier(nom_fichier)
    liste_tailles_mots = []
    for mot in liste_mots:
        taille = len(mot)
        liste_tailles_mots.append(taille)
    return liste_tailles_mots


def nb_caractere_fichier(nom_fichier): #renvoie le nombre de caracteres d'un texte dnas un fichier .txt
    with open(nom_fichier, "r", encoding="utf-8") as f:
        texte = f.read()
    return len(texte)



#%% Utile partout : 

def calcul_cout(texte, L):                     #fonction qui calcule le cout d'une liste de str avec la longueur L d'une ligne.
    cout = 0                                   #on initialise
    for ligne in texte:                        #le cout total est la somme des couts des chaques lignes
        cout += (L - len(ligne))**2            #definition du cout d'une ligne
    return cout

#%% Algorithme exhaustif sans backtracking, parfaitement absurde de complexité qui sert juste pour les graphiques

def exhaustif(liste_mots, L): #avec L=60, fonctionne pour environ 180 mots (en une vingtaine de sec)

    cout_opt = float('inf')    #on cherche a minimiser le cout S, donc on demarre avec un cout infini et on va le fai évoluer
    texte_opt = None        #on stocke ici la liste des lignes str qu'on renverra
                    
    texte = [liste_mots[0]]       #on initialise le texte, il devra forcement commencer par le premier mot
    mots_restants = liste_mots[1:]
    
    texte_opt, cout_opt = aux_exhaustif(texte, texte_opt, cout_opt, mots_restants, L)
    
    return texte_opt, cout_opt 

def aux_exhaustif(texte, texte_opt, cout_opt, mots_restants, L): #fonction auxiliaire recursive
    
    if len(mots_restants) == 0:             #si on a finit le texte
        cout = calcul_cout(texte, L)              #on calcule le cout
        if cout < cout_opt:                       #on verifie si c'est plus optimal que la solution précedente
            cout_opt = cout                       #on assigne
            texte_opt = texte
        return texte_opt, cout_opt
    
    # a chaque étape, 2 choix max, soit le mot d'apres rentre dans la ligne (parfois impossible), soit on fait un retour
    mot_a_caler = mots_restants[0]
    if len(texte[-1]) + 1 + len(mot_a_caler) <= L:                  #on verifie deja si ca peut rentrer avec l'espace restant en fin de ligne
        texte_bis = texte[:-1] + [texte[-1] + ' ' + mot_a_caler]    #on le cale a la fin de la derniere ligne
        texte_opt, cout_opt = aux_exhaustif(texte_bis, texte_opt, cout_opt, mots_restants[1:], L) 
        
    texte_opt, cout_opt = aux_exhaustif(texte + [mot_a_caler], texte_opt, cout_opt, mots_restants[1:], L) #on créé une nouvelle ligne
    
    return np.array(texte_opt), cout_opt


#%% Algorithme exhaustif avec backtracking

def exhaustif_backtracking(liste_mots, L): #avec L=60, fonctionne pour environ 180 mots (en une vingtaine de sec)

    cout_opt = float('inf')    #on cherche a minimiser le cout S, donc on demarre avec un cout infini et on va le fai évoluer
    texte_opt = None        #on stocke ici la liste des lignes str qu'on renverra
                    
    texte = [liste_mots[0]]       #on initialise le texte, il devra forcement commencer par le premier mot
    mots_restants = liste_mots[1:]
    
    texte_opt, cout_opt = aux_exhaustif_backtracking(texte, texte_opt, cout_opt, mots_restants, L)
    
    return texte_opt, cout_opt 

def aux_exhaustif_backtracking(texte, texte_opt, cout_opt, mots_restants, L): #fonction auxiliaire recursive
    
    if len(mots_restants) == 0:             #si on a finit le texte
        cout = calcul_cout(texte, L)              #on calcule le cout
        if cout < cout_opt:                       #on verifie si c'est plus optimal que la solution précedente
            cout_opt = cout                       #on assigne
            texte_opt = texte
        return texte_opt, cout_opt
    
    if calcul_cout(texte[:-1], L) > cout_opt:     #un peu de backtracking, si meme alors que c'est pas fini mais c'est déja plus couteux, on arrete de chercher
        return texte_opt, cout_opt
    
    # a chaque étape, 2 choix max, soit le mot d'apres rentre dans la ligne (parfois impossible), soit on fait un retour
    mot_a_caler = mots_restants[0]
    if len(texte[-1]) + 1 + len(mot_a_caler) <= L:                  #on verifie deja si ca peut rentrer avec l'espace restant en fin de ligne
        texte_bis = texte[:-1] + [texte[-1] + ' ' + mot_a_caler]    #on le cale a la fin de la derniere ligne
        texte_opt, cout_opt = aux_exhaustif_backtracking(texte_bis, texte_opt, cout_opt, mots_restants[1:], L) 
        
    texte_opt, cout_opt = aux_exhaustif_backtracking(texte + [mot_a_caler], texte_opt, cout_opt, mots_restants[1:], L) #on créé une nouvelle ligne
    
    return np.array(texte_opt), cout_opt


#%% Algorithme glouton

def ajouter_mot(texte, mot, L):
    """ 
    On ajoute le mot là où on peut l'ajouter
    Soit en fin de ligne si il reste de la place pour le mot et un espace
    Soit dans une nouvelle ligne si il n'y a plus la place
    """
    if len(texte) == 0:
        # Si on est au début du texte (=si le texte est vide) alors on ajoute le mot
        texte.append(mot)
        return texte
    if len(texte[-1]) < L - len(mot):
        # Si il reste assez de place pour un mot et un espace alors on et le mot en fin de ligne
        texte[-1] += " " + mot
    else:
        # Si la ligne est pleine, alors on en crée une nouvelle
        texte.append(mot)
    return texte

def glouton(liste_mots, L):
    """
    Algorithme glouton pour la résolution du problème 2
    --> Dès qu'on peut placer un mot on le place 
    """
    # On parcourt le texte à l'envers pour pouvoir pop() le premier pop
    # On aurait pu utiliser une file
    texte = liste_mots[::-1]
    texte_opt = []
    # Tant que le texte d'origine n'est pas vide on continue
    while len(texte): 
        mot = texte.pop()
        texte_opt = ajouter_mot(texte_opt, mot, L)
    return texte_opt, calcul_cout(texte_opt, L)


#%% Algorithme récursif simple

""" 
Ce programme calcule le cout de mise en page minimum avec une approche recursive
"""

def algo_recursif(liste_tailles_mots,L,i=0):
    if i==len(liste_tailles_mots):                           #Cas de base : le mot d'indice len(liste_taille_mots) n'existe pas
        return 0                                             # donc le cout de la placer est nul.
     
    cout_opt = []                                            #On initialise la liste qui contiendra pour un indice i les couts possibles a partir de i
    for j in range(i,len(liste_tailles_mots)):               #Pour tous les mots a partir de i jusqu'a la fin
        longueur = 0                                         
        for m in range(i,j+1):                               #On test d'ajouter les j-1 premiers mots après i 
            longueur += liste_tailles_mots[m]                #on ajoute le mot m
        longueur += (j-i)                                    #on prend en compte les espaces   
        if longueur <= L:                                    #si la ligne est valide, on peut calculer son cout
            cout_ligne = (L-longueur)**2                    #calcul du cout de la ligne
            cout_total = cout_ligne + algo_recursif(liste_tailles_mots, L,j+1)   #calcul du cout total pour les mots de i à j sur la même ligne
            cout_opt.append(cout_total)                     #on ajoute ce cout dans la liste
       
    return min(cout_opt)                                     #on retourne le cout minimum pour placer les mots a partir de l'indice i

#%% Algorithme récursif avec mémoisation


""" 
Ce programme calcule le cout de mise en page minimum
"""

def memo_cout_optimal(liste_tailles_mots, L, i=0, d=None):
    
    if d is None:                                              
        d = {}

    if i == len(liste_tailles_mots):
        return 0

    if i in d:                          #si le coup à partir de l'indice i à déja été calculé, on le retourne directement.
        return d[i]

    cout_opt = []
    longueur = 0
    j = i
    while j<len(liste_tailles_mots) and longueur + liste_tailles_mots[j] + (j-i) <= L:     #Pour tout les mots a partir de i jusqu'a ce qu'il y ait trop de caractères sur la ligne
        
        longueur += liste_tailles_mots[j]
        
        
        cout_ligne = (L - (longueur + (j-i))) ** 2
        cout_total = cout_ligne + memo_cout_optimal(liste_tailles_mots, L, j+1, d)
        cout_opt.append(cout_total)
        j+=1

    d[i] = min(cout_opt)
    return d[i]




#%% Algorithme itératif (Programmation dynamique)

""" 
Ce programme calcule le cout de mise en page minimum et renvoie la mise en page correspondante.
"""


def dico_to_texte(liste_mots,L,i=0,d=None):

    liste_tailles_mots = [len(mot) for mot in liste_mots]   #crée une liste avec les tailles de chaque mot du texte
    
    if d is None:
        d = {}
                                          #On initialise les dictionnaires au début
    fin_ligne = {}                                

    d[len(liste_tailles_mots)]=0          #Cela correspond au cas de base de l'algorithme recursif
    for i in range(len(liste_tailles_mots)-1,-1,-1):

        meilleur_j = None                     #meilleur_j correspond à l'indice du dernier mot sur la ligne du mot i pour un cout minimal
        cout_opt = float('inf')              #cout_opt correspond au cout minimal, il est initialisé à +infini pour qu'il soit modifié dès la première comparaison 
        longueur = 0                      
        j = i
        
        while j<len(liste_tailles_mots) and longueur + liste_tailles_mots[j] + (j-i) <= L:


            longueur += liste_tailles_mots[j]


            cout_ligne = (L - (longueur + (j-i))) ** 2
            cout_total = cout_ligne + d[j+1]             #application de la relation de récurrence
            if cout_total < cout_opt :                   # si cette configuration à un cout plus faible, elle devient la solution optimale 
                cout_opt = cout_total                    # tant qu'une autre configuration de cout inferieur n'est pas trouvée
                meilleur_j = j                           

            j+=1

        fin_ligne[i]=meilleur_j                          #On enregistre dans un dictionnaire l'indice du dernier mot sur la ligne, pour pouvoir reconstruire ensuite le texte
        d[i] = cout_opt                                  #On enregistre aussi le cout, comme dans l'algorithme avec mémoisation

    texte_form = ''                                      #initialisation du texte
    while i<len(liste_tailles_mots):                     #tant que on a pas traité tout les mots
        ligne = liste_mots[i]                           #la ligne commence par le mot d'indice i
        j = i+1                             
        while j<=fin_ligne[i]:                          #on ajoute tout les mots jusqu'a l'indice indiqué par le dictionnaire
            ligne += ' ' + liste_mots[j]                #sans oublier aussi les espaces entre chaque mot
            j+=1
        texte_form += ligne + (L - len(ligne)) * ''+'\n'  #Une fois qu'on a écris la ligne, on rajoute les espaces pour combler la ligne et on saute une ligne
        i = j                                       #On passe ensuite à la ligne suivante        

    return texte_form,d[0]




#%% Tests et affichages

def affiche_texte(texte_opt, L): #fonction qui permet de visualiser la solution trouvée en affichant le texte et en montrant les espaces a la fin des lignes
    
    for ligne in texte_opt:      
        a = len(ligne)
        print(ligne + (L-a)*'_') #on complete la ligne par des '_'
        
    print("\nCout =", calcul_cout(texte_opt, L))
    return


def test_texte(liste_mots, L, programme, tronquer = False): #fonction qui permet de tester nos programme sur un texte (sous forme de liste de mots) (que l'on peut tronquer si il est trop long)
    
    if tronquer != False and isinstance(tronquer, int): #si on veut tronquer et que 'tronquer' doit etre un int
        liste_mots = liste_mots[:tronquer]            #on prend uniquement les 'tronquer' premiers mots (afin de travailler avec des complexité plus faible)
        
    start = time.time()                                  #on s'interesse aux temps d'execution
    texte_opt, cout_opt = programme(liste_mots, L)  	 #on appele le programme a tester pour creer le texte optimal
    end = time.time()
    
    # affiche_texte(texte_opt, L)
    print(f"{programme.__name__} :")
    print(f"  → Coût = {cout_opt}")
    print(f"  → Temps d'exécution = {end - start:.3f} secondes") #avec 3 décimales
    print()
    return





#%% Graphiques du temps d'execution : 
    
def graphique_temps_execution_en_fonction_de_N(liste_mots, L, N_max, programme, pas=1):
    if N_max > len(liste_mots):
        N_max = len(liste_mots)
        
    N = list(range(1, N_max + 1, pas))
    temps_execution = []

    for i in N:
        start = time.time()
        T, S = programme(liste_mots[:i], L)
        end = time.time()
        temps_execution.append(end - start)
        # print(i)

    plt.plot(N, temps_execution)
    plt.xlabel('Nombre de mots')
    plt.ylabel("Temps d'exécution (s)")
    titre = f"Temps d'exécution de {programme.__name__} en fonction du nombre de mots"
    plt.title(titre)
    plt.savefig(titre + 'png')  # Sauvegarde du graphique
    plt.show()  
    
'''
graphique_temps_execution_en_fonction_de_N(recherche_complet, 60, 100000, dico_to_texte, 100)
graphique_temps_execution_en_fonction_de_N(recherche_complet, 60, 100000, glouton, 100)
graphique_temps_execution_en_fonction_de_N(recherche_complet, 60, 26, exhaustif, 3)
graphique_temps_execution_en_fonction_de_N(recherche_complet, 60, 160, exhaustif_backtracking, 1)
'''


