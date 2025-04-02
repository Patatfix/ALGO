def tri_rdv(demandes): #trie les rdv par ordre d'heure de début et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
    
    n = len(demandes)
    
    demandes_classées = [[demande[i], i] for i in range(n)] #on ajoute un indice pour pouvoir ranger a la fin dans l'ordre original
    
    demandes_classées = sorted(demandes_classées, key = lambda x: x[0][0]) #on trie par heure de début de rdv

    return (demandes_classées)