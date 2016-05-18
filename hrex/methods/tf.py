#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
**TF**: The model based on the frequency takes into account the number of times a word occur
in the whole collection as an indicative of generalization-specialization. The idea in this model is
that the more general a word, the higher its frequency. This model uses the list of terms extracted
using documents as contexts. For each word, the resulting frequency is the sum of all individual
frequencies in documents.

@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('methods.tf')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from structure.methods import AbstractMethod
 
class TF(AbstractMethod):
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
            id1, tf1 = self.dwords[w1]
            for j in xrange(i+1, len(keys)):
                w2 = keys[j]
                id2, tf2 = self.dwords[w2]
                if w1 != w2:
                    if tf1 > tf2:
                        self.rels.append((w1, w2))
                    elif tf2 > tf1:
                        self.rels.append((w2, w1))
#End of class TF
