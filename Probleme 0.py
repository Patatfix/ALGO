def tri_rdv(demandes, borne_de_tri = "début"): #trie les rdv par ordre d'heure de début et ajoute un indice pour retrouver l'ordre initial des rdv dans la variable demandes
    #bornes_de_tri peut etre "début" ou "fin"
    n = len(demandes)
    
    if isinstance(demandes, tuple) == True: #verifie si il y a déja l'indice de tri ou non
        demandes_classées = [[demandes[i], i] for i in range(n)] #si non, on ajoute un indice pour pouvoir ranger a la fin dans l'ordre original
    else : 
        demandes_classées = demandes #si oui
        
    if borne_de_tri == "début" : 
        demandes_classées = sorted(demandes_classées, key = lambda x: x[0][0]) #on trie par heure de début de rdv
    elif borne_de_tri == "fin": 
        demandes_classées = sorted(demandes_classées, key = lambda x: x[0][1]) #si on veut trier par heure de fin de rdv

    return (demandes_classées)