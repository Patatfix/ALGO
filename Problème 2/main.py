# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 15:22:23 2025

@author: Noreddine
"""
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

texte1 = lire_fichier("reccherche_p1.txt")
print(len(texte1))


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

#%% Tests
texte = "je suis une patate chaude et j'aime les patates"

texte_opt = ["Je suis une patate", "chaude et j'aime", "les patates"]

vers_fichier_texte(texte_opt, "Texte_opti.txt")

    