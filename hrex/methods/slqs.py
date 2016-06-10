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

import numpy as np

from structure.methods import AbstractMethod
 
class SLQS(AbstractMethod):
    """
    Identify hierarchical relations using the SLQS algorithm.
    """
    def __init__(self, dwords=None, dctxs=None, drels=None):
        """
        Initiates the class SLQS

        Parameters:
        -----------
        dwords : DicWords
            Dictionary of words in the form:
                word: (id, df)
        dctxs : DicWords
            Dictionary of contexts in the form:
                ctx: (id, df)
        drels : DicRels
            Dictionary of relations in the form:
                (idw, idc): weight
            where `weight` is a LMI - MinMax scored

        Notes:
        ------
        AbstractMethod sets default values and contains the precision, 
        recall and f-measure

        self.rels : list
            A list containing the Hypernym-hyponym relations found by the method. 
            The list has the form:
                [(idH_1, idh_1), (idH_2, idh_2), ...]

        self.gsrels : list
            A list containing the relations found in a gold standard.
        """
        default = {'window': 5, 'lex_mode':'lemma', 'cwords':True, 'ctw':'n', 'normalize':True, 'lower':True}
        AbstractMethod.__init__(self, default=default)
        self.dwords = dwords
        self.dctxs = dctxs
        self.drels = drels
        self.rels = []
        self.gsrels = []


    def _buildMeanEntropy(self):
        """
        Calculate the mean entropy from `self.dctxs` to `self.dwords`,
        associating each word with the mean of the entropy of its contexts.
        """
        # use ids as keys to self.dctx
        dctx_t = self.dctxs.id2key()
        for w in self.dwords:
            idw, _ = self.dwords[w]
            
            lctx = self.drels.getContexts(idw)
            ent = []
            for idc in lctx:
                _, e = dctx_t[idc]
                ent.append(e)
            ent = np.asarray(ent)
            self.dwords.setFreq(w, np.mean(ent))
        del self.dctxs
        del self.drels


    def identifyRelations(self):
        """
        Identify relations between terms based on the model. This function 
        uses self.dwords and self.drels in order to find the most hierarchical 
        related terms.

        Notes:
        ------
        In this method, the dictionary `drels` contains the positive pointwise 
        mutual information `ppmi` instead of the term frequency `tf` associated 
        to the term and context. The relations found by the method are saved 
        into self.rels
        """
        # calculate the mean entropy for words
        self._buildMeanEntropy()
        
        keys = self.dwords.keys()
        for i in xrange(len(keys)):
            w1 = keys[i]
            idw1, e1 = self.dwords[w1]
            for j in xrange(i+1, len(keys)):
                w2 = keys[j]
                idw2, e2 = self.dwords[w2]

                if e1 and e2:
                    slqs = 1 - (float(e1)/e2)

                    if slqs > 0:
                        self.rels.append((w2, w1))
                    elif slqs < 0:
                        self.rels.append((w1, w2))
#End of class SLQS
