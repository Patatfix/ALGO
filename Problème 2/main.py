import numpy as np

def lire_fichier(nom_fichier):
    with open("recherche_p1.txt", "r", encoding="utf-8") as f:
        texte = f.read()
        try:
            if texte[-1] == '\n':
                texte = texte[:-1]
            texte = texte.replace("\n", " ")
            mots = texte.split(' ')
        except : 
            raise ValueError("Fichier de coordonnées mal formé")
    return mots

def liste_taille(nom_fichier):
    liste_mots = lire_fichier(nom_fichier)
    T = []
    for mot in liste_mots:
        taille = len(mot)
        T.append(taille)
    return T

def calcul_S(texte, L):
    S = 0
    for ligne in texte:
        S += (L - len(ligne))**2
    return S

def vers_fichier_texte(texte_opti, nom_fichier):
    fichier = open(nom_fichier, "a")
    for ligne in texte_opti:
        fichier.write(str(ligne) + "\n")
    fichier.close()
    return

def liste_erreur(solution, L):
    erreur = []
    for i in range(len(solution)):
        erreur.append((L - solution[i])**2)
    return erreur

# %% Exhaustif

def exhaustif(texte, L):
    if texte[-1] == '\n':
        texte = texte[:-1]
    mots = texte.split(' ')
    n = len(mots)
    tailles_mots = [len(mot) for mot in mots]

    S_opt = float('inf')
    texte_opt = None
    
    texte = [mots[0]]
    mots_restants = mots[1:]
    
    texte_opt, S_opt = aux_exhaustif(texte, texte_opt, S_opt, mots_restants, L)
    return texte_opt, S_opt

def aux_exhaustif(texte, texte_opt, S_opt, mots_restants, L):
    
    if len(mots_restants) == 0: #si on a finit le texte
        S = calcul_S(texte, L)
        if S < S_opt:           #on verifie si c'est optimal
            S_opt = S
            texte_opt = texte
        return texte_opt, S_opt
    
    if calcul_S(texte[:-1], L) > S_opt:               #backtracking, si meme alors que c'est pas fini, 
        return texte_opt, S_opt
    
    #2 cas, soit le mot d'apres rentre dans la ligne, soit on fait un retour
    mot_a_caler = mots_restants[0]
    if len(texte[-1]) + 1 + len(mot_a_caler) <= L: #on verifie deja si ca peut rentrer avec l'espace, si on a le choix
        texte_bis = texte[:-1] + [texte[-1] + ' ' + mot_a_caler]
        texte_opt, S_opt = aux_exhaustif(texte_bis, texte_opt, S_opt, mots_restants[1:], L)
        
    texte_opt, S_opt = aux_exhaustif(texte + [mot_a_caler], texte_opt, S_opt, mots_restants[1:], L)
    
    return np.array(texte_opt), S_opt


def affiche_texte(texte_opt, L):
    for ligne in texte_opt:
        a = len(ligne)
        print(ligne + (L-a)*'_')
        
    print("\n\nS =", calcul_S(texte_opt, L))
    return

# %% Glouton

def ajouter_mot(solution, mot):
    if len(solution) == 0:
        solution.append(mot)
        return solution
    if len(solution[-1]) < L - len(mot):
        solution[-1] += " " + mot
    else:
        solution.append(mot)
    return solution

def glouton(texte, L):
    texte_r = texte[::-1]
    solution = []
    while len(texte_r): 
        mot = texte_r.pop()
        solution = ajouter_mot(solution, mot)
    return solution

# %% avant_apres


def avant_apres(texte, L, reverse=False):
    if not reverse:
        texte_r = texte[::-1]
    else:
        texte_r = texte
    solution = []
    while len(texte_r):
        mot = texte_r.pop()
        if len(solution) == 0:
            solution.append(mot)
        elif len(solution[-1]) + 1 + len(mot) == L:
            solution.append(mot)
        elif len(solution[-1]) < L - len(mot) and (len(mot)>= 3 or len(solution[-1] + " " + mot) < L - len(texte_r[-1])):
            solution[-1] += " " + mot
        elif len(solution[-1]) < L - len(mot):
            s1 = avant_apres(texte_r + [mot], L, True)
            s2 = avant_apres(texte_r, L, True)
            s = solution.copy()
            s[-1] += " " + mot
            cs1, cs2 = calcul_S(solution + s1, L), calcul_S(s + s2, L)

            if cs1 > cs2:
                return s + s2
            else:
                return solution + s1
        else:
            solution.append(mot)
    return solution
    


# %% Test

# Test recursive
import sys

sys.setrecursionlimit(100000)

L = 20
rec_p1 = lire_fichier("recherche_p1.txt")
recursive_p1 = recursive(rec_p1, L)
cSolution = calcul_S(recursive_p1, L)
affiche_texte(recursive_p1, L)
print(cSolution)
print("\n")

# Texte glouton
L = 20
rec_p1 = lire_fichier("recherche_p1.txt")

solution = glouton(rec_p1, L)
cSolution = calcul_S(solution, L)
affiche_texte(solution, L)
print(cSolution)
print("\n")

# Test avant_apres

L = 20
t = lire_fichier("test_court.txt")
solution = avant_apres(rec_p1[:100], L)
cSolution = calcul_S(solution, L)

affiche_texte(solution, L)
print(cSolution)