#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains filters for terms and dictionaries.

@author: granada
"""
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments
import logging
logger = logging.getLogger('corpus.filters')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from operator import itemgetter

from structure import dictionaries

def filter_topN(dic, N=1000):
    """
    Filter out terms in a dictionary and keep only the topN 
    containing the greatest number of contexts.

    Parameters:
    -----------
    dic : dictionaries.dictWords
        Dictionary in the form `word: (id, tf)`
    N : int
        Number of terms in dictionary with more contexts

    Returns:
    --------
    dtopN : dictionaries.DictWords
        Dictionary containing only the top N terms
    """
    logger.info('filtering top %d words from dictionary' % N)
    dtopN = dictionaries.DictWords()
    sizes = []
    for w in dic:
        id, tf = dic[w]
        sizes.append((w, tf))
    ar_topN = sorted(sizes, key=itemgetter(1), reverse=True)[:N]
    topNids = dict(ar_topN).keys()
    for w in topNids:
        idw, tf = dic[w]
        dtopN[w] = (idw, tf)
    logger.info('dictionary reduced from %d to %d words' % (len(dic), len(dtopN)))
    return dtopN


def filterTF(dic, min_tf=5):
    """
    Remove contexts under certain frequency (tf).

    Parameters:
    -----------
    dic : dictionaries.DictWord
        Dictionary in the form `word: (id, tf)`

    Returns:
    --------
    dmin_tf: dictionaries.DictWord()
        Dictionary containing only terms with `tf` > `min_tf`
    """
    logger.info('filtering out terms under %d occurrences' % min_tf)
    dmin_tf = dictionaries.DictWords()
    for word in dic:
        id, tf = dic[word]
        if tf >= min_tf:
            dmin_tf[word] = (id, tf)
    logger.info('dictionary reduced from %d to %d words' % (len(dic), len(dmin_tf)))
    return dmin_tf


def filterTopNContexts(dic, N=50):
    """
    Filter out contexts of the dictionary, keeping only the top N 
    most associated contexts to each term. `dic` is filtered by
    the weight associated between term and context.

    Parameters:
    -----------
    dic : dictionaries.DictRels
        Dictionary of relations in the form `(idw, idc): weight`
    N : int
        Number of associated contexts in the final dictionary

    Returns:
    --------
    dftr : dictionaries.DictRels
        Dictionary containing the filtered contexts
    """
    dftr = dictionaries.DictRels()
    dw = dic.dic2List(key='idw', transposed=False)
    for idw in dw:
        dftr[idw] = sorted(dw[idw], key=itemgetter(1), reverse=True)[:N]
    return dftr
