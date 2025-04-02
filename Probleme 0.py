def optim_planning_v0(demandes, rdv = (0,0)):
    h0, hmax = 0, 10**9
    n = len(demandes)
    demandes_classées = [[demande[i], i] for i in range(n)] #on ajoute un indice pour pouvoir ranger a la fin dans l'ordre original
    demandes_classées = sorted(demandes_classées, key = lambda x: x[0][0]) #on trie par heure de début de rdv

    
    
    

    
    
    demandes_classées = sorted(demandes_classées, key = lambda x: x[1])  #on remet dans l'ordre original  
    return (planning) #on renvoie une liste de doublet (liste de rdv)