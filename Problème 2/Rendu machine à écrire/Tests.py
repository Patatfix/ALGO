# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 22:36:26 2025

@author: remyg
"""

import main
import time

#%% Pour faire les tests : 
    
recherche_p1 = main.lire_fichier("recherche_p1.txt")
exemple1 = main.lire_fichier("exemple1.txt")
recherche_complet = main.lire_fichier("recherche_complet.txt")
#%% Tests et comparaisons des différents algorithmes

main.test_texte(recherche_p1, 60, main.exhaustif_backtracking, 150)
main.test_texte(recherche_p1, 60, main.glouton, 150)
main.test_texte(recherche_p1, 60, main.dico_to_texte, 150)

#%% Comparaison des algorithmes utilisant la structure récursive

#Exemple du cours, petit
print('→ EXEMPLE COURT')
print('')
T_exemple1 = main.liste_taille_fichier('exemple1.txt')
L_exemple1 = main.lire_fichier(('exemple1.txt'))
#Le cout minimal est censé être 110

start = time.time()
cout = main.algo_recursif(T_exemple1,20)
end = time.time()
print('')
print(f"l'algoritme recursif simple trouve un cout minimum = {cout} pour exemple1 en {end-start} secondes")

start = time.time()
cout = main.memo_cout_optimal(T_exemple1,20)
end = time.time()
print('')
print(f"l'algoritme recursif avec mémoisation trouve un cout minimum = {cout} pour exemple1 en {end-start} secondes")

start = time.time()
texte,cout = main.dico_to_texte(L_exemple1, 20)
end = time.time()
print('')
print(f"l'algoritme dynamique trouve un cout minimum = {cout} pour exemple1 en {end-start} secondes")
print('')

#Exemple moyen

print('→ EXEMPLE MOYEN')
print('')


#Le cout minimal est censé être 797

T_recherche_p1 = main.liste_taille_fichier('recherche_p1.txt')
L_recherche_p1 = main.lire_fichier(('recherche_p1.txt'))

start = time.time()
k = main.memo_cout_optimal(T_recherche_p1,80)
end = time.time()
print('')
print(f"l'algoritme recursif avec mémoisation trouve un cout minimum = {k} pour exemple1 en {end-start} secondes")

start = time.time()
texte,cout = main.dico_to_texte(L_recherche_p1,80)
end = time.time()
print('')
print(f"l'algoritme dynamique trouve un cout minimum = {cout} pour exemple1 en {end-start} secondes")

print('')
#Exemple Long

print('→ EXEMPLE LONG')
print('')

T_recherche_long = main.liste_taille_fichier('recherche_complet.txt')[:800000]
L_recherche_long = main.lire_fichier(('recherche_complet.txt'))[:800000]

start = time.time()
k = main.memo_cout_optimal(T_recherche_long,80)
end = time.time()
print('')
print(f"l'algoritme recursif avec mémoisation trouve un cout minimum = {k} pour exemple1 en {end-start} secondes")

start = time.time()
texte,cout = main.dico_to_texte(L_recherche_long,80)
end = time.time()
print('')
print(f"l'algoritme dynamique trouve un cout minimum = {cout} pour exemple1 en {end-start} secondes")
#%% Mettre en page le texte complet dans la console


start = time.time()
texte,cout = main.dico_to_texte(recherche_complet, 80)
print(texte)
print(f"le cout de la mise en page est de {cout}")
end = time.time()
print(f"Temps d'éxecution de l'algorithme dynamique : {end-start} secondes")

#%% Mettre en page le texte complet dans un fichier externe

start = time.time()
texte,cout = main.dico_to_texte(recherche_complet, 80)

end = time.time()
print(f"Temps d'éxecution de l'algorithme dynamique : {end-start} secondes")

#Coller le texte mis en page dans un fichier externe

nom_fichier = "Texte complet.txt"
with open(nom_fichier, "w", encoding="utf-8") as fichier:
    fichier.write(texte)
