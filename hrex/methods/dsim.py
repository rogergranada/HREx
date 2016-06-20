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
of a term. The code implementing these measures are freely available by 
[Weeds](https://github.com/SussexCompSem/learninghypernyms) :cite:`WeedsEtAl2014`.

@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('methods.dsim')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np

from structure.methods import AbstractMethod
from utils import mathutils


class DSim(AbstractMethod):
    """
    Identify hierarchical relations using the DSim algorithm.
    This is an abstract class to be inherited by methods that 
    implement DSim.
    """
    def __init__(self, dwords=None, drels=None):
        """
        Initiates the class DSim

        Parameters:
        -----------
        dwords : DicWords
            Dictionary of words in the form:
                word: (id, df)
        drels : DicRels
            Dictionary of relations in the form:
                (idw, idc): tf

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
        default = {'window': 5, 'lex_mode':'lemma', 'cwords':True, 'ctw':'n', 
                   'normalize':True, 'lower':True}
        AbstractMethod.__init__(self, default=default)
        self.dwords = dwords
        self.drels = drels


    def _buildVectors(self, l1, l2):
        """
        Transform lists into an intersection like lists.

        Parameters:
        -----------
        l1 : array_like
            list containing contexts and frequencies
        l2 : array_like
            list containing contexts and frequencies

        Returns:
        --------
        v1 : array_like
            list containing the intersection-like of elements
        v1 : array_like
            list containing the intersection-like of elements
        both : array_like
            list of elements in both lists

        Examples:
        ---------
        >>> u = [(1, 1), (2, 2), (3, 3)]
        >>> v = [(2, 20), (3, 30), (4, 40)]
        >>> v1, v2, both = DSim()._buildVectors(u, v)
        >>> v1
            [2, 3]
        >>> v2
            [20, 30]
        >>> both
            [2, 3]
        """
        d1 = dict(l1)
        d2 = dict(l2)
        bothkeys = set(d1.keys()).union(d2.keys())

        v1 = np.array([], dtype=np.float64)
        v2 = np.array([], dtype=np.float64)
        for id in bothkeys:
            if d1.has_key(id):
                v1 = np.append(v1, d1[id])
            else:
                v1 = np.append(v1, 0)
            if d2.has_key(id):
                v2 = np.append(v2, d2[id])
            else:
                v2 = np.append(v2, 0)
        return v1, v2, list(bothkeys)


    def _intersectedFeatures(self, l1, l2):
        """
        Get the values of the intersection of two vectors. 

        Parameters:
        -----------
        l1 : array_like
            list containing frequencies of contexts
        l2 : array_like
            list containing frequencies of contexts

        Returns:
        --------
        both_u : array_like
            List containing elements of l1 that appear in both lists
        both_v : array_like
            List containing elements of l2 that appear in both lists

        Examples:
        ------
        >>> u = [10, 0, 5]
        >>> v = [20, 30, 2]
        >>> v1, v2 = DSim()._intersectedFeatures(u, v)
        >>> v1
            [10, 5]
        >>> v2
            [20, 2]
        """
        both = (l1 != 0) & (l2 != 0)
        return l1[both], l2[both]
 

class Weeds(DSim):
    """
    Identify hierarchical relations using the Weeds et al. (2004) algorithm.
    H1: If $w_1$ entails $w_2$ then the characteristics of $w_1$ also appear in $w_2$;
    H2: If all the features of $w_1$ appear in $w_2$, then $w_1$ entails $w_2$ [2,3].
    WeedsPrec is defined as:
        WeedsPrec(u,v) = \frac{\sum_{f \in (F_u \cap F_v)}w_u(f)}
                              {\sum_{f \in (F_u)}w_u(f)}
        WeedsRec(u,v) = \frac{\sum_{f \in (F_u \cap F_v)}w_v(f)}
                              {\sum_{f \in (F_u)}w_v(f)}
    where $F_x$ is the set of features of a term $x$, and $w_x(f)$ is the weight of
    the feature $f$
    [2] Weeds, J., Weir, D.: A general framework for distributional similarity. 
        In: Proceedings of the 2003 conference on Empirical methods in natural 
        language processing (EMNLP '03). Association for Computational Linguistics, 
        Stroudsburg, PA, USA, 81-88, 2003. http://dx.doi.org/10.3115/1119355.1119366.
    [3] Weeds, j., Weir, D., McCarthy, D.: Characterising measures of lexical 
        distributional similarity. In: Proceedings of the 20th international 
        conference on Computational Linguistics (COLING '04). Association for 
        Computational Linguistics, Stroudsburg, PA, USA, 2004,
        http://dx.doi.org/10.3115/1220355.1220501
    """
    def __init__(self, dwords=None, drels=None):
        """
        Initiates the class Weeds

        Parameters:
        -----------
        dwords : DicWords
            Dictionary of words in the form:
                word: (id, df)
        drels : DicRels
            Dictionary of relations in the form:
                (idw, idc): ppmi
            where ppmi is the Positive Pointwise Mutual Information

        Notes:
        ------
        DSim sets default values and contains the precision, recall and f-measure

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
        self.drels = drels
        self.rels = []
        self.gsrels = []
        

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
        drels = self.drels.dic2List()
        keys = self.dwords.keys()
        for i in xrange(len(keys)):
            w1 = keys[i]
            id1, df1 = self.dwords[w1]
            ctx1 = drels[id1]
            for j in xrange(i+1, len(keys)):
                w2 = keys[j]
                id2, df2 = self.dwords[w2]
                ctx2 = drels[id2]

                v1, v2, vboth = self._buildVectors(ctx1, ctx2)
                #prec, rec = mathutils.WeedsPrecRec(v1, v2)
                both_v1, both_v2 =self._intersectedFeatures(v1, v2)
                weedsprec = both_v1.sum() / v1.sum()
                weedsrec = both_v2.sum() / v2.sum()

                if weedsprec > weedsrec:
                    self.rels.append((w2, w1))
                elif weedsrec > weedsprec:
                    self.rels.append((w1, w2))
#End of class Weeds


class ClarkDE(DSim):
    """
    Clarke [4] formalised the idea of distributional generality and computes the
    entailment between two words using a variation of Weeds et al. [2,3] measures.
    The measure differs from the one proposed by Weeds et al. because it reduces
    the weight of included features if they have lower weight within the vector of 
    the broader term. Precision (ClarkeDEPrec) and recall (ClarkeDERec) are defined as:


    ClarkeDEPrec(u, v) = \frac{\sum_{f \in F_u \cap F_v}min(I(u,f), I(v,f))}
                              {\sum_{f \in F_u}I(u, f)}
    ClarkeDERec(u, v)  = \frac{\sum_{f \in F_u \cap F_v}min(I(u,f), I(v,f))}
                              {\sum_{f \in F_v}I(v, f)}

    [4] Daoud Clarke. Context-theoretic semantics for natural language: An overview. 
        In Proceedings of the Workshop on Geometrical Models of Natural Language Semantics, 
        GEMS ’09, pages 112–119. Association for Computational Linguistics, 2009.
    """
    def __init__(self, dwords=None, drels=None):
        """
        Initiates the class ClarkeDE

        Parameters:
        -----------
        dwords : DicWords
            Dictionary of words in the form:
                word: (id, df)
        drels : DicRels
            Dictionary of relations in the form:
                (idw, idc): ppmi
            where ppmi is the Positive Pointwise Mutual Information

        Notes:
        ------
        DSim sets default values and contains the precision, recall and f-measure

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
        self.drels = drels
        self.rels = []
        self.gsrels = []
        

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
        drels = self.drels.dic2List()
        keys = self.dwords.keys()
        for i in xrange(len(keys)):
            w1 = keys[i]
            id1, df1 = self.dwords[w1]
            ctx1 = drels[id1]
            for j in xrange(i+1, len(keys)):
                w2 = keys[j]
                id2, df2 = self.dwords[w2]
                ctx2 = drels[id2]

                v1, v2, vboth = self._buildVectors(ctx1, ctx2)
                both_v1, both_v2 =self._intersectedFeatures(v1, v2)

                numerator = 0
                for i in range(len(both_v1)):
                    value = min(both_v1[i], both_v2[i])
                    numerator += value
                clarkeprec = numerator / v1.sum()
                clarkerec = numerator / v2.sum()

                if clarkeprec > clarkerec:
                    self.rels.append((w2, w1))
                elif clarkerec > clarkeprec:
                    self.rels.append((w1, w2))
#End of class ClarkDE

