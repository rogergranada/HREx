#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains an abstract class to methods. This class should be
inherited by classes that implement a method to extract hierarchical
relations.

A method starts from a list of words, contexts and their frequencies

@author: granada
"""

from collections import namedtuple
P = namedtuple('P', ['lex_mode', 'cwords', 'ctw', 'normalize', 'lower', 'window'])

class AbstractMethod(object):
    """
    Abstract class that implements a method of extracting hierarchical
    relations from text.
    """
    def __init__(self, default=None):
        """
        Initiate the elements of the class.

        Notes:
        --------
        self.prec : float
            The precision score
        self.rec : float
            The recall score
        self.fscore : float
            The F-measure
        self.rels : array_like
            A list containing all relations
        self.gsrels : list
            A list containing the relations found in a gold standard.
        """
        self.prec = None
        self.rec = None
        self.fscore = None
        self.rels = []
        self.gsrels = []
        self.settings = None
        if default:
            self._setDefault(default)


    def _setDefault(self, default):
        """
        Set default parameters to a method.
        
        Parameters:
        -----------
        default :
            The list of parameters to be set
        """
        p = [('lex_mode', ''), ('cwords', True), ('ctw', ''), ('normalize', True), 
             ('lower', True), ('window', 0)]
        par = []
        for el, val in p:
            if default.has_key(el):
                par.append(default[el])
            else:
                par.append(val)
        self.settings = P(*par)


    def defaultSettings(self):
        """
        The default settings of the method.

        Returns:
        --------
        dict()
            A dictionary containing the default parameters used by the method
        """
        return self.settings


    def identifyRelations(self):
        """
        Identify relations between terms based on the model. This function 
        uses self.dwords, self.dctxs and/or self.drels in order to find the
        most hierarchical related terms.
        """ 


    def precision(self, GS):
        """
        Parameters:
        -----------
        gs : GoldStandard instance
            The gold standard to evaluate the precision

        Returns:
        --------
        self.precision : float
            The precision score calculated when comparing
            with a gold standard (GS):
                $$\frac{elements in method \cap elements in GS}{elements in method}$$
        """
        if not self.gsrels:
            self.gsrels = GS(self.dwords).allRelations()
        if not self.rels:
            self.identifyRelations()
        intersect = set(self.gsrels).intersection(set(self.rels))
        if len(self.rels) != 0:
            self.prec = float(len(intersect))/len(self.rels)
        else:
            self.prec = 0.0
        return self.prec


    def recall(self, gs):
        """
        Parameters:
        -----------
        gs : GoldStandard instance
            The gold standard to evaluate the precision

        Returns:
        --------
        self.recall : float
            The recall score calculated when comparing
            with a gold standard (GS):
                $$\frac{elements in method \cap elements in GS}{elements in GS}$$
        """
        if not self.gsrels:
            self.gsrels = GS(self.dwords).allRelations()
        if not self.rels:
            self.identifyRelations()
        intersect = set(self.gsrels).intersection(set(self.rels))
        if len(self.gsrels) != 0:
            self.rec = float(len(intersect))/len(self.gsrels)
        else:
            self.rec = 0.0
        print self.gsrels
        return self.rec


    def fmeasure(self, GS):
        """
        Parameters:
        -----------
        GS : GoldStandard instance
            The gold standard to evaluate the precision

        Returns:
        --------
        fmeasure : float
            The F-measure score  calculated as:
            $$\frac{2 \times P \times F}{P + F}$$
        """
        if not self.prec:
            self.precision(GS)
        if not self.rec:
            self.recall(GS)
        self.fscore = (2*self.prec*self.rec)/(self.prec+self.rec)
        return self.fscore


    def getRelations(self):
        """
        Returns:
        --------
        self.rels : array_like
            All relations found by the method. Relations should be in
            the form [(H_1, h_1), (H_2, h_2), ..., (H_n, h_n)] where
            `H` is the hypernym and `h` is the hyponym term. 
        """
        return self.rels


    def getGSRelations(self):
        """
        Returns:
        --------
        self.gsrels : array_like
            All relations found by the gold standard. Relations should be in
            the form [(H_1, h_1), (H_2, h_2), ..., (H_n, h_n)] where
            `H` is the hypernym and `h` is the hyponym term. 
        """
        return self.gsrels
#End of class MethodInterface


    




