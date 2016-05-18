#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
**DSim**: The model based on Directional Similarity takes into account the Distributional Inclusion
Hypothesis, according to which the contexts of a narrow term are also shared by the broad term.
 
This model uses the list of terms and contexts extracted using a window of size=5. The degree of 
association between terms and contexts is determined by a weight function. Thus, the value of the 
frequency of a term with a context is replaced by its Positive Pointwise Mutual Information (PPMI) 
:cite:`ChurchHanks1990` value, where all negative values are set to zero. Directional similarity 
can be tested using the measure proposed by Weeds et al. :cite:`WeedsEtAl2004`.

$$
WeedsPrec(u, v) = \frac{\sum_{f \in F_u \cap F_v}I(u,f)}{\sum_{f \in F_u}I(u, f)} 
$$
$$
WeedsRec(u, v) = \frac{\sum_{f \in F_u \cap F_v}I(v,f)}{\sum_{f \in F_v}I(v, f)}
$$

or the measure proposed by Clarke :cite:`Clarke2009`. 

$$
ClarkeDEPrec(u, v) = \frac{\sum_{f \in F_u \cap F_v}min(I(u,f), I(v,f))}{\sum_{f \in F_u}I(u, f)}
$$
$$
ClarkeDERec(u, v) = \frac{\sum_{f \in F_u \cap F_v}min(I(u,f), I(v,f))}{\sum_{f \in F_v}I(v, f)}
$$

These measures can identify taxonomic relations between terms using the notion of precision and recall 
of a term. The code implementing these measures are freely available by [Weeds](https://github.com/SussexCompSem/learninghypernyms)
:cite:`WeedsEtAl2014`.

@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('methods.dsim')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from structure.methods import AbstractMethod
 
class DSim(AbstractMethod):
    """
    Identify hierarchical relations using the DF algorithm.
    """
    def __init__(self, dwords=None):
        """
        Initiates the class DF

        Parameters:
        -----------
        dwords : DicWords
            Dictionary of words in the form:
                word: (id, df)

        Notes:
        ------
        MethodInterface sets default values and contains the precision, recall and f-measure

        self.rels : list
            A list containing the Hypernym-hyponym relations found by the method. 
            The list has the form:
                [(idH_1, idh_1), (idH_2, idh_2), ...]

        self.gsrels : list
            A list containing the relations found in a gold standard.
        """
        default = {'lex_mode':'lemma', 'cwords':True, 'ctw':'n', 'normalize':True, 'lower':True}
        AbstractMethod.__init__(self, default=default)
        self.dwords = dwords

        self.rels = []
        self.gsrels = []


    def identifyRelations(self):
        """
        Identify relations between terms based on the model. This function 
        uses self.dwords, self.dctxs and/or self.drels in order to find the
        most hierarchical related terms.

        Notes:
        ------
        In this method, the dictionary `dwords` contains the document frequency
        `df` instead of the term frequency `tf` associated to the term.
        The relations found by the method are saved into self.rels
        """
        keys = self.dwords.keys()
        for i in xrange(len(keys)):
            w1 = keys[i]
            id1, df1 = self.dwords[w1]
            for j in xrange(i+1, len(keys)):
                w2 = keys[j]
                id2, df2 = self.dwords[w2]
                if w1 != w2:
                    if df1 > df2:
                        self.rels.append((w1, w2))
                    elif df2 > df1:
                        self.rels.append((w2, w1))
#End of class DF
