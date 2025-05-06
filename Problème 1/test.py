# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 20:12:47 2025

@author: romai
"""
import util
import main
import time
import numpy as np
import matplotlib.pyplot as plt


#%% Recupération des exemples 



exemple1 = util.lire_fichier_coords('exemple1.txt')
exemple2 = util.lire_fichier_coords('exemple2.txt')
exemple3 = util.lire_fichier_coords('exemple3.txt')
exemple4 = util.lire_fichier_coords('exemple4.txt')




#%% Test exemple 1

glouton1 = main.parcours_glouton(exemple1)
glouton2 = main.parcours_glouton2(exemple1,1)
util.affiche_tournee(glouton1)
util.affiche_tournee(glouton2)




#%% Test exemple 2

glouton1 = main.parcours_glouton(exemple2)
"""On voit avec cette methode que on gagne 2 unité distance sur le glouton ^pour alpha=0.5
Mais ce code n'est pas très efficace pour ce type de donnée et erreur """

"""Utilise une methode améliorer de glouton, on peut faire varier alpha pour trouver une meilleur solution"""
glouton2 = main.parcours_glouton2(exemple2,0.5)

start = time.time()
tournee = main.dicho(exemple2)
util.affiche_tournee(tournee)
end = time.time()
print("Temps d'éxécution pour la méthode dicho sur l'exemple 2", round(end-start, 3), "secondes")


util.affiche_tournee(glouton1)
util.affiche_tournee(glouton2)

"""Test recuit simulé avec glouton basique"""
"""
solution = main.recuit_simulé(glouton1,main.voisin2,100000,3,main.f4)
util.affiche_tournee(solution)
"""
# %% Isocèle


tournee = main.dicho(exemple3)
util.affiche_tournee(tournee)




#%% Test exemple 4

"""Essayer en changeant alpha avec 1,2,3,4 pour le parcours_glouton2"""

glouton1 = main.parcours_glouton(exemple4)
glouton2 = main.parcours_glouton2(exemple4,4)
tournee = main.dicho(exemple4)
util.affiche_tournee(tournee)
util.affiche_tournee(glouton1)
util.affiche_tournee(glouton2)

#%% Test Recuit simulé avec glouton pondéré puis heuristique locale
"""
main.test_recuit(exemple1,50000,2,main.f2,main.voisin2)
"""
#%% tests algo exhaustif
"""
n = 11 #trop long a partir de n = 12

start = time.time()
chemin,_ = main.calcul_tournee_exhaustif(exemple2[:n])
end = time.time()

print(chemin, '\nL\'algo a pris',end - start,'secondes à s\'executer')
util.affiche_tournee(chemin)

"""
#%% Défaillance glouton

print("Graphe qui montre la défaillance de glouton")
arbres_test_glouton_défaillant = util.lire_fichier_coords("exemple_défaillant_2.txt")

tournee_gloutonne_défaillante = main.parcours_glouton(arbres_test_glouton_défaillant)
tournee_exhaustive = main.calcul_tournee_exhaustif(arbres_test_glouton_défaillant)


util.affiche_tournee(tournee_gloutonne_défaillante)
util.affiche_tournee(tournee_exhaustive[0])



#%% Test inverser arbres
print("Test inverser arbres")

tournee_gloutonne = main.parcours_glouton(exemple2)

start = time.time()
tournee_inverse_arbre = main.inverser_arbres(tournee_gloutonne)
end = time.time()

print("Test inverser arbres temps d'éxécution : ",end - start)
util.affiche_tournee(tournee_inverse_arbre)


#%% test inverse 2 arete
print("test inverse 2 arete")

tournee_gloutonne = main.parcours_glouton(exemple2)

start = time.time()
tournee_inverse_arete = main.inverse_arete(tournee_gloutonne)
end = time.time()

util.affiche_tournee(tournee_inverse_arete)
print("Test inverse 2 arrêtes, temps d'éxécution : ",end - start)


#%% Tests inverse 3 aretes

print("Tests inverse 3 aretes")
"""
tournee_gloutonne = main.parcours_glouton(exemple2)

start = time.time()

tournee_inverse_3_arete = main.inverse_3_arete(tournee_gloutonne)

end = time.time()

util.affiche_tournee(tournee_inverse_3_arete)
print("Test inverse 3 arrêtes, temps d'éxécution : ",end - start)

"""
#%% graphique temps d'execution de l'algo exhaustif 
"""
n_max = 8
temps_execution = []
nombre_d_arbres = list(range(n_max))


total_arbres = len(exemple2)

for i in range(n_max):
    indices = np.random.choice(total_arbres, size=i, replace=False)
    arbres_test = [exemple2[j] for j in indices]
    start = time.time()
    chemin = main.calcul_tournee_exhaustif(arbres_test)
    end = time.time()
    temps_execution.append(end - start)
    
plt.plot(nombre_d_arbres, temps_execution)
plt.xlabel("Nombre d'arbres")
plt.ylabel("Temps d'exécution (s)")
plt.title("Temps d'exécution en fonction du nombre d'arbres")
plt.savefig("temps d'execution exhaustif.png")
plt.show()
"""

#%% Analyse en fonction du nombre de points

print("Analyse en fonction du nombre de points")
# x = nombre de points à tester
x = np.linspace(10, 100, 10, dtype=int)  # 10 valeurs entières entre 10 et 500
y = []

for n in x:
    
    donnees = main.creer_donnees(n, -10, 10)
    s1 = main.evaluation(donnees)
    start = time.time()
    parcours = main.recuit_puis_inverse_arete(s1)
    end = time.time()
    y.append(end - start)
    print(n)

# Tracé du temps d'exécution en fonction du nombre de points
plt.plot(x, y, marker='o')
plt.title("Temps d'exécution vs nombre de points")
plt.xlabel("Nombre de points")
print(f"temps d'exécution = {end-start}")
end = time.time()

#%% Graphe de temps d'execution des fonctions heuristique
"""
print("Graphe de temps d'execution des fonctions heuristique")
fonction_a_tester = main.inverse_arete
n = 95

temps_execution = []
nombre_d_arbres = [i for i in range(n)]

for i in range(n):
    tournee = main.parcours_glouton(exemple2[:i])
    start = time.time()
    tournee = fonction_a_tester(tournee)
    end = time.time()
    temps_execution.append(end - start)
    print(i,n)
    
plt.plot(nombre_d_arbres, temps_execution)
plt.xlabel("Nombre d'arbres")
plt.ylabel("Temps d'exécution (s)")
plt.title("Temps d'exécution en fonction du nombre d'arbres")
plt.savefig("temps d'execution {fonction_a_tester}.png")
plt.show()
"""



#%%Test qui on aidé pour l'implémentation

#main.test_evaluation(100, "exemple2.txt")

#main.compare_temperature(main.f1, main.f2, main.f3, main.f4, 10)

#new = main.voisin3(main.parcours_glouton(exemple2))
#print(new)     
#util.affiche_tournee(new)
