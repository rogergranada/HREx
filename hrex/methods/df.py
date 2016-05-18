#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
**DF**: The model based on the document frequency takes into account the number of documents
in which a word appears as an evidence of taxonomic relation. Thus, a word that occurs in more
documents tends to be more general than a word that appears in few documents.

@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('methods.df')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from structure.methods import AbstractMethod
 
class DF(AbstractMethod):
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
