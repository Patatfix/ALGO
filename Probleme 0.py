# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:22:52 2025

@author: Noreddine
"""
import random
Hmax = 10000

def crée_demandes(n,Hmax):
    demandes = []
    for i in range(n):
        hdeb = random.randint(0, Hmax)
        hfin = random.randint(hdeb, Hmax)
        while hfin == hdeb:
            hfin = random.randint(hdeb, Hmax)
        demandes.append((hdeb,hfin))
    return demandes

demandes = crée_demandes(10, Hmax)
    

def tri_rdv(demandes, borne_de_tri = "début"): #trie les rdv par ordre d'heure de début et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
    #bornes_de_tri peut etre "début" ou "fin"
    n = len(demandes)
    
    demandes_classées = [[demandes[i], i] for i in range(n)] #on ajoute un indice pour pouvoir ranger a la fin dans l'ordre original
    
    if borne_de_tri == "début" : 
        demandes_classées = sorted(demandes_classées, key = lambda x: x[0][0]) #on trie par heure de début de rdv
    elif borne_de_tri == "fin": 
        demandes_classées = sorted(demandes_classées, key = lambda x: x[0][1]) #si on veut trier par heure de fin de rdv

    return (demandes_classées)

tri_rdv(demandes)