# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:22:52 2025

@author: Noreddine
"""
import random
Hmax = 10000

def crée_demandes(n, Hmax= 10000):

    demandes = []

    for i in range(n):
        hdeb = random.randint(0, Hmax - 1)    # Ici
        hfin = random.randint(hdeb, Hmax)
        while hfin == hdeb:
            hfin = random.randint(hdeb, Hmax)
        demandes.append((hdeb,hfin))

    return demandes

demandes = crée_demandes(10, Hmax)
    

def tri_rdv(demandes, borne_de_tri = "début"): #trie les rdv par ordre d'heure de début et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
    #bornes_de_tri peut etre "début", "fin" ou "longueur"
    n = len(demandes)

    if borne_de_tri == "début" : 
        demandes_classées = sorted(demandes, key = lambda x: x[0]) #on trie par heure de début de rdv
    elif borne_de_tri == "fin": 
        demandes_classées = sorted(demandes, key = lambda x: x[1]) #si on veut trier par heure de fin de rdv
    elif bornes_de_tri == "longueur croissante":
        demandes_classées = sorted(demandes, key = lambda x: abs(x[0] - x[1])) #si on veut trier par durée du rdv croissante
    elif bornes_de_tri == "longueur décroissante":
        demandes_classées = sorted(demandes, key = lambda x: abs(x[0] - x[1])) #si on veut trier par durée du rdv decroissante
        demandes_classées.reverse()
    else : 
        print("aucun tri effectué, borne_de_tri invalide")

    return (demandes_classées)

demandes_classées = tri_rdv(demandes)
print(demandes_classées)
total=[[]]

def compatible_planning(planning, creneau): # 
    for cre in planning:
        if not compatible(cre, creneau):
            return False
    return True  

def compatible(creneau_1, creneau_2): # Vérifie que deux créneaux sont compatible ensemble
    if (creneau_1[0] >= creneau_2[0] and creneau_1[0] <= creneau_2[1]) or (creneau_1[1] >= creneau_2[0] and creneau_1[1] <= creneau_2[1]):
        return False
    return True


#%% 
def enumeration_exhaustive(demandes, curr=[],i=0,d=0,total = []):
    planning=[]
    
    
    if i == len(demandes):
        total.append(curr[:])
        if d == len(demandes)-1:
            #print(d)
            s = len(total[0])
            #print(total)
            planning.append(total[0])
            for p in total[1:]:
                
                
                if len(p) > s:
                   planning.append(p)
                   s = len(p)
            return planning[-1]
        
        return enumeration_exhaustive(demandes, [], d + 1, d + 1, total)
    
    
    if compatible_planning(curr, demandes[i]):
        curr.append(demandes[i])
        res = enumeration_exhaustive(demandes,curr,i+1,d,total)
        if res:
            return res
        curr.pop()
    
    return enumeration_exhaustive(demandes,curr,i+1,d,total)

print(enumeration_exhaustive(demandes_classées))


