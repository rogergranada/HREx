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


def filterDictionaries(dwords, dctxs, drels, dwf, startid=1):
    """
    Filter IDs from dictionaries keeping only terms contained in `dwf`.
    Non-related contexts and relations are removed from `dctxs` and
    `drels`.

    Parameters:
    -----------
    dwf : dictionaries.DicWords
        Dictionary of filtered words, being a subset of the `dwords`
    startid : int
        Initial id used in the dictionary

    Returns:
    ------
    `dwfl` : dictionaries.DicWords
        Dictionary containing the words from `dwf` with new ids
    `dcfl` : dictionaries.DicWords
        Dictionary containing the contexts of the words in `dwf`
    `drfl` : dictionaries.DicRels
        Dictionary containing the relations of the words in `dwf`
    """
    dctx_t = dctxs.id2key()
    dwfl = dictionaries.DictWords(startid=startid)
    dcfl = dictionaries.DictWords(startid=startid)
    drfl = dictionaries.DictRels()

    words = dwords.keys()
    for w in sorted(words):
        idw, _ = dwords[w]
        lctx = drels.getContexts(idw)
        for idc in lctx:
            tf = drels[(idw, idc)]
            ctx, _ = dctx_t[idc]
            dcfl[ctx] = 1
            dwfl[w] = 1
            nidw, _ = dwfl[w]
            nidc, _ = dcfl[ctx]
            drfl[(nidw, nidc)] = tf
            del drels[(idw, idc)]
        del dwords[w]
    return (dwfl, dcfl, drfl)
