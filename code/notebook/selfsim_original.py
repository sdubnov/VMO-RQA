#!/usr/bin/env python2.7

import numpy as np
import sys
from Resources.PyOracle.FactOracle import get_distance 
import itertools

def create_selfsim(oracle, method = 'compror'): 
    """ Create self similarity matrix from compror codes or suffix links
    """
    len_oracle = oracle.n_states - 1
    mat = np.zeros((len_oracle, len_oracle))
    if method == 'compror':
        if oracle.code == []:
            print "Codes not generated. Generating codes with encode()."
            oracle.encode()
        ind = 0
        inc = 1
        for l, p in oracle.code:
            if l == 0:
                inc = 1
            else:
                inc = l
            if inc >= 1:
                for i in range(l):
                    mat[ind+i][p+i-1] = 1
                    mat[p+i-1][ind+i] = 1
            ind = ind + inc
    elif method == 'suffix':
        for i, s in enumerate(oracle.sfx):
            while s != None and s != 0:
                mat[i-1][s-1] = 1
                mat[s-1][i-1] = 1 
                s = oracle.sfx[s] 
    elif method == 'rsfx':
        latent = infer_latent_var(oracle)
        for i in range(len(latent)):
            _l = latent[i]
            p = itertools.product(_l, repeat = 2)
            for _p in p:
                mat[_p[0]-1][_p[1]-1] = 1            
    return mat
    
def infer_latent_var(oracle):
    """ Return lists of states connected by suffix links"""
    l = []
    for k in oracle.rsfx[0]:
        tmp = []
        tmp.append(k)
        _c = oracle.rsfx[k][:]
        while _c != []:
            _k = _c.pop(0)
            tmp.append(_k)
            _c.extend(oracle.rsfx[_k])
        l.append(tmp)
    return l
