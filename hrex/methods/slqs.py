#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
**SLQS**: The model based on entropy was developed by Santus et al. \cite{SantusEtAl2014} 
and relies on the idea that superordinate terms are less informative than their hyponyms. 
This model also uses the list of terms and contexts extracted using a window of `size=K`. 
SLQS model employs Local Mutual Information (LMI) to weight co-occurrences as well as uses 
entropy as an estimate of context informativeness. After extracting co-occurrences and 
weighting them using LMI, the `N` most associated contexts are identified using the Shannon 
entropy measure \cite{Shannon1948}, where `N` is usually set to 50. The resulting values of 
entropy are normalized using the Min-Max-Scaling in a range 0--1. Finally, the entropy of a 
word is defined as the median entropy of its `N` contexts as:

$$E_{wi} = Me_{j=1}^{N} (H_n(c_j))$$

where entropy is defined as:

$$H(c) = - \sum_{i=1}^{n} p(f_i|c) \cdot log_2(p(f_i|c))$$

where $p(f_i|c)$ is the probability of the feature $f_i$ given the context $c$, obtained 
through the ratio between the frequency of $\langle c, f_i\rangle$ and the total frequency 
of $c$. Finally, *SLQS* measures the semantic generality of word $u$ and word $v$ as the 
reciprocal difference between the semantic generality of the two words $u$ and $v$ as: 

$$SLQS(u, v) = 1 - \frac{E_{u}}{E_{v}}$$

According to the formula, $u$ subsumes $v$ if *SLQS* > 0, $v$ subsumes $u$ if *SLQS* < 0, 
and we can not infer a taxonomic relationship between $u$ and $v$ if *SLQS* $\simeq$ 0.

@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('methods.slqs')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Set standard output encoding to UTF-8.
from codecs import getwriter, open
sys.stdout = getwriter('UTF-8')(sys.stdout)

from structure.methods import AbstractMethod
 
class SLQS(AbstractMethod):
    """
    Identify hierarchical relations using the SLQS algorithm.
    """
    def __init__(self):
        pass


