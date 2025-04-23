# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 15:02:24 2025

@author: romai
"""
import numpy as np


def lire_fichier(nom_fichier):
    with open(nom_fichier, "r", encoding="utf-8") as f:
        texte = f.read()
        try:
            if texte[-1] ==  '\n':
                texte = texte[:-1]
            texte = texte.replace("\n", " ")
            mots = texte.split(" ")
        except : 
            raise ValueError("Fichier de coordonnées mal formé")
    return mots

def calcul_S(texte, L):
    S = 0
    for ligne in texte:
        S += (L - len(ligne))**2
    return S

#%% Algo glouton

def layout_glouton(texte,L=20):
    lignes=[texte[0]]
    m = len(texte[0])
    texte = texte[1:]
    for mot in texte:
        n = len(mot)
        assert n<=L, 'Un mot est plus grand que la largeur de la page'
        if n+m+1 <= L:
            lignes[-1] +=  " " + mot
            m += n+1
        else:
            lignes.append(mot)
            m=n
    score = calcul_S(lignes, L)
    return lignes,score
        

#%% Algo exhaustif

def layout_exhaustif(texte, L):
    n = len(texte)
    tailles_mots = [len(mot) for mot in texte]
    S_opt = float('inf')
    texte_opt = None
    lignes = [texte[0]]
    mots_restants = texte[1:]
    texte_opt, S_opt = aux_exhaustif(lignes, texte_opt, S_opt, mots_restants, L)
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

#%% Algo récurive

def recursive(texte, L, solution=[]):
    # Cas de base
    if len(texte) == 0:
        return solution
    
    # Cas général
    mot = texte[0]
    if len(solution) == 0:
        solution.append(mot)
        return recursive(texte[1:], L, solution)
    s = solution.copy()
    s[-1] += " " + mot
    R1 = recursive(texte[1:], L, s)
    R2 = recursive(texte, L, solution)
    C1 = (L-(len(solution[-1])+ len(mot)))**2 + calcul_S(R1, L)
    C2 = (L-(len(solution[-1])))**2 + calcul_S(R2, L)
    if C1 < C2:
        return R1
    else:
        return R2

#%%Memoïsation

def layout_aux(texte,L):
    dico ={}
    n = len(texte)
    tailles_mots = [len(mot) for mot in texte]
    S_opt = float('inf')
    texte_opt = None
    lignes = [texte[0]]
    mots_restants = texte[1:]
    texte_opt, S_opt = aux_exhaustif(lignes, texte_opt, S_opt, mots_restants, L, dico)
    return texte_opt, S_opt

def aux_aux(texte, texte_opt, S_opt, mots_restants, L, dico):
    if len(mots_restants) == 0: #si on a finit le texte
        S = calcul_S(texte, L)
        if S < S_opt:           #on verifie si c'est optimal
            S_opt = S
            texte_opt = texte
        return texte_opt, S_opt
    if calcul_S(texte[:-1], L) > S_opt:               #backtracking, si meme alors que c'est pas fini, 
        return texte_opt, S_opt
    mot_a_caler = mots_restants[0]
    if len(texte[-1]) + 1 + len(mot_a_caler) <= L: #on verifie deja si ca peut rentrer avec l'espace, si on a le choix
        texte_bis = texte[:-1] + [texte[-1] + ' ' + mot_a_caler]
        texte_opt, S_opt = aux_aux(texte_bis, texte_opt, S_opt, mots_restants[1:], L)
    texte_opt, S_opt = aux_aux(texte + [mot_a_caler], texte_opt, S_opt, mots_restants[1:], L)
    return np.array(texte_opt), S_opt



#%% fonction d'affichage

def affiche_texte(texte_opt, L):
    for ligne in texte_opt:
        a = len(ligne)
        print(ligne + (L-a)*'_')
    return