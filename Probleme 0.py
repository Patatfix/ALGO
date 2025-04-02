# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:22:52 2025

@author: Noreddine
"""

def compatible(creneau_1, creneau_2):
    if (j[0] <= dim[0] and j[0] <= dim[1]) or (j[1] <= dim[0] and j[1] <= dim[1]):
        return False
    return True

def compatible_planning(planning, creneau):
    for j in planning:
        if not compatible(j, creneau):
            return False
    return True