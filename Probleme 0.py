# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:22:52 2025

@author: Adrien
"""

def compatible(creneau_1, creneau_2):
    if (creneau_1[0] <= creneau_2[0] and creneau_1[0] <= creneau_2[1]) or (creneau_1[1] <= creneau_2[0] and creneau_1[1] <= creneau_2[1]):
        return False
    return True

def compatible_planning(planning, creneau):
    for j in planning:
        if not compatible(j, creneau):
            return False
    return True

