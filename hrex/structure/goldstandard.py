#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains an abstract class to gold standards. This class should be
inherited by classes that implement a gold standard.

@author: granada
"""

class AbstractGoldStd(object):
    """
    Abstract class that use a gold standard to compare terms.
    """
    def __init__(self, dwords=None):
        """
        Initiate the elements of the class.
        
        Parameters:
        -----------
        dwords : dictionaries.DicWords
            A dictionary containing all words extracted from files

        Notes:
        ------
        In case that `dwords` is passed as argument, a set for each term 
        containing its hypernyms will be created calling `_loadSynsets`.

        self.dHset : dict
            Dictionary containing the set of synsets hypernyms of the term `key`
            The dictionary has the form:
                idw: set(synset_H1, synset_H2, ...)
        self.dwsyn : dict
            Dictionary containing the set of words from synsets in which the term
            occurs. The dictionary has the form:
                idw: set(lemma_1, lemma_2, ...) 
        """
        self.dwords = dwords
        
        self.dHset = {}
        self.dwsyn = {}

        if dwords:
            self._loadSynsets()


    def _loadSynsets(self):
        """
        Identify the existent relations in the gold standard to terms that
        appear in `self.dwords`.

        Returns:
        -----------
        self.dHset : dict
            Dictionary containing the set of synsets hypernyms of the term `key`
            The dictionary has the form:
                idw: set(synset_H1, synset_H2, ...)
        self.dsyn : dict
            Dictionary containing the set of synset ids in which the term
            occurs. The dictionary has the form:
                idw: set(synset_1, synset_2, ...) 
        """
        pass


    def getHypernymsOf(self, key, mode='id'):
        """
        Return a set contaning all hypernyms of ``key''.
    
        Parameters:
        ----------
        key : string, int
            The key of the self.dHset
        mode : string {'id', 'word'}
            The type of `key`
        """
        if mode == 'id':
            idw = key
        elif mode == 'word':
            idw, _ = self.dwords[key]
        return self.dHset[idw]


    def isHypernym(self, v1, v2, mode='id'):
        """
        Verify wether ``v1'' is hypernym of ``v2''. 

        Parameters:
        -----------
        v1 : string, int
            The hypernym candidate
        v2 :
            The hyponym candidate
        mode : string {'id', 'word'}
            The type of `v1` and `v2`

        Returns:
        --------
        boolean {True, Fase}
            The existence or not of the relation
        """
        if mode == 'id':
            idw1 = v1
            idw2 = v2
        elif mode == 'word':
            idw1 = self.dwords[v1]
            idw2 = self.dwords[v2]
        sw2 = self.dHset[idw2]
        if sw2.intersection(self.dsyn[idw1]):
            return True
        else:
            return False


    def allHypernyms(self, word):
        """
        Return all hypernyms of a certain word when it is a noun.

        Parameters:
        -----------
        word : string
            A noun to extract the hypernyms

        Returns:
        --------
        allHyp : array_like
            A list containing all the hypernyms
        """
        pass


    def hasWord(self, word):
        """
        Verify whether or not ``word`` is in the gold standard.

        Parameters:
        -----------
        word : string
            A noun to extract the hypernyms

        Returns:
        --------
        exists : boolean {True, False}
            True if the gold standard has the word, False otherwise
        """
        pass


    def filterDictionary(self, dic):
        """
        Filter out words that not appear in the gold standard.
        Return a new dictionary containing only terms that
        appear in the gold standard.

        Parameters:
        -----------
        dic: dictionaries.DictWords
            Dictionary containing word to be filtered

        Returns:
        --------
        dicf: dictionaries.DictWords
            Filtered dictionary
        """
        pass


    def allRelations(self):
        """
        Using the dictionary `self.dwords`, `allRelations`` returns a list
        containing all relations between terms of the dictionary found by
        the gold standard.

        Returns:
        --------
        rels : array_like
            List of all hierarchical relations between terms of the dictionary
        """
        pass
#End of AbstractGoldStd
