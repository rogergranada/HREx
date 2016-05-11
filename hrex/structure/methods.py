#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains an abstract class to methods. This class should be
inherited by classes that implement a method to extract hierarchical
relations.

A method starts from a list of words, contexts and their frequencies

@author: granada
"""

class MethodInterface(object):
    """
    Interface to classes that implements a method of extracting hierarchical
    relations from text.
    """
    def __init__(self):
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
        """
        self.prec = None
        self.rec = None
        self.fscore = None
        self.rels = []


    def precision(self):
        """
        Returns:
        --------
        self.precision : float
            The precision score calculated when comparing
            with a gold standard (GS):
                $$\frac{elements in method \cap elements in GS}{elements in method}$$
        """
        return self.prec


    def recall(self):
        """
        Returns:
        --------
        self.recall : float
            The recall score calculated when comparing
            with a gold standard (GS):
                $$\frac{elements in method \cap elements in GS}{elements in GS}$$
        """
        return self.rec


    def fmeasure(self, gold_standard):
        """
        Returns:
        --------
        fmeasure : float
            The F-measure score  calculated as:
            $$\frac{2 \times P \times F}{P + F}$$
        """
        if not self.prec:
            self.precision(gold_standard)
        if not self.rec:
            self.recall(gold_standard)
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
#End of class MethodInterface


    




