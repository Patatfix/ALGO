# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:22:52 2025

@author: Noreddine
"""

def enumeration_exhaustive(demandes, lenSol=0):
    N = len(demandes)
    Solution = []
    for i in range(N):
        dim = dimension.pop(i)
        Solution.append(dim)
        enumeration_exhaustive(demandes, lenSol + 1)
    
        dim.insert(0, demandes[i])
    return Solution
