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
    
def tri_rdv(demandes): #trie les rdv par ordre d'heure de dÃ©but et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
    
    n = len(demandes)
    
    demandes_classes = [[demandes[i], i] for i in range(n)] #on ajoute un indice pour pouvoir ranger a la fin dans l'ordre original
    
    demandes_classes = sorted(demandes_classes, key = lambda x: x[0][0]) #on trie par heure de dÃ©but de rdv

    return demandes_classes

tri_rdv(demandes)