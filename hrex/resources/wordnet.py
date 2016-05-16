#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module compares relations extracted by a method against the WordNet
gold standard. This version uses [NLTK WordNet](http://www.nltk.org/howto/wordnet.html).
Thus, before running wordnet.WordNet, make sure that you have NLTK installed in your
machine with WordNet downloaded.

@author: granada
""" 
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('resources.wordnet')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from nltk.corpus import wordnet as wn

from structure.goldstandard import AbstractGoldStd
from structure import dictionaries

class WordNet(AbstractGoldStd):
    """
    Class that interacts with WordNet gold standard. WordNet 3.0 from NLTK is
    called in this class. 
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
            Dictionary containing the set of lemmas from synsets in which the term
            occurs. The dictionary has the form:
                idw: set(lemma_1, lemma_2, ...) 
        """
        AbstractGoldStd.__init__(self, dwords)


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
        logger.info('accepted dictionary containing %d words' % len(self.dwords))
        logger.info('verifying relations in WordNet')
        for word in self.dwords:
            if self.hasWord(word):
                id, _ = self.dwords[word]
                self.dwsyn[id] = self.allLemmas(word)
                self.dHset[id] = self.allHypernyms(word)
        logger.info('found %d words in WordNet' % len(self.dwsyn))
        logger.info('reducing dictionary: %d to %d' % (len(self.dwords), len(self.dHset)))


    def allLemmas(self, word):
        """
        Return all lemmas associated to a synset containing ``word''.

        Parameters:
        -----------
        word : string
            A noun to extract the hypernyms

        Returns:
        --------
        lemmas : array_like
            A list containing all lemmas
        """
        lemmas = [word]
        for syn in wn.synsets(word, pos=wn.NOUN):
            lemmas = [w for w in syn.lemma_names()]
            lemmas.extend(lemmas)
        return set(lemmas)


    def allHypernyms(self, word):
        """
        Return all hypernyms of a certain word when it is a noun.

        Parameters:
        -----------
        word : string
            A noun to extract the hypernyms

        Returns:
        --------
        allHyp : set_like
            A set containing all the hypernyms
        """
        allHyp = []
        syns = wn.synsets(word, pos=wn.NOUN)
        allsyn = []
        for syn in syns:
            H = [w for s in syn.closure(lambda s:s.hypernyms()) for w in s.lemma_names()]
            allHyp.extend(H)
            allsyn.extend(syn.instance_hypernyms())
        for syn in allsyn:
            allHyp.extend(syn.lemma_names())
            H = [w for s in syn.closure(lambda s:s.hypernyms()) for w in s.lemma_names()]
            allHyp.extend(H)
        return set(allHyp)


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
            idw1, _ = self.dwords[v1]
            idw2, _ = self.dwords[v2]
        sw2 = self.dHset[idw2]
        if sw2.intersection(self.dwsyn[idw1]):
            return True
        else:
            return False


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
        if wn.synsets(word, pos=wn.NOUN):
            return True
        return False


    def filterDictionary(self, dic=None):
        """
        Filter out words that not appear in the gold standard.
        Return a new dictionary containing only terms that
        appear in the gold standard.

        Parameters:
        -----------
        dic: dictionaries.DictWords, optional
            Dictionary containing word to be filtered

        Returns:
        --------
        dicf: dictionaries.DictWords
            Filtered dictionary

        Notes:
        ------
        In case of there is not a `dic`, the filter occurs in `self.dwords`
        """
        if not dic:
            if self.dwords:
                dic = self.dwords
            else:
                logger.error('a dictionary must be passed as argument')
                sys.exit(1)
        
        logger.info('verifying terms in WordNet')
        dicf = dictionaries.DictWords()
        for word in dic:
            if self.hasWord(word):
                id, tf = dic[word]
                dicf[word] = (id, tf)
        logger.info('found %d words in WordNet' % len(dicf))
        logger.info('reducing dictionary: %d to %d' % (len(dic), len(dicf)))
        return dicf


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
        rels = []
        dic = self.dwords
        dicf = self.filterDictionary()
        
        for w1 in dicf:
            for w2 in dicf:
                if w1 != w2 and self.isHypernym(w1, w2, mode='word'):
                    rels.append((w1, w2))
        logger.info('found %d relations in WordNet' % len(rels))
        return rels
#End of Wordnet
