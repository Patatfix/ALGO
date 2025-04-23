# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 15:40:08 2025

@author: romai
"""
import probleme_2

texte1 = probleme_2.lire_fichier("recherche_p1.txt")[:]

glouton, score_glouton = probleme_2.layout_glouton(texte1,20)
#exhaustif, score_exhaustif= probleme_2.layout_exhaustif(texte1, 20)

probleme_2.affiche_texte(glouton,20)
print(f"Voici le score pour le glouton : {score_glouton}")
#probleme_2.affiche_texte(exhaustif,20)
#print(f"Voici le score pour l'exhaustif : {score_exhaustif}")