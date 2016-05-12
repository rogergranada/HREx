#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
**INRIASAC**: The model based on the frequency of a term in a document when occurring with
other terms in the same sentence \cite{Grefenstette2015}, and is meant to capture the 
intuition that general terms are more widely distributed than more specific terms (e.g., 
dog appears in more Wikipedia articles than poodle).

The original version of this algorithm uses a Porter stemmed version of the terms while here
we can use raw or lemmas to process the method. Thus, let $D(term)$ be the document frequency 
of a term in the corpus. Let $SentCooc(term_i, term_j)$ be the number of times that the $term_i$ 
and $term_j$ appear in the same sentence in the corpus. Given two terms, $term_i$ and $term_j$,
if $term_i$ appears in more documents than $term_j$, then $term_i$ is a candidate hypernym for 
$term_j$. 

```
CandHypenym(term_i) = { term_j :
    SentCooc(term_i, term_j ) > 0 &&
    D(term_j) > D(term_i)
```

Next the best hyperym candidate is defined for $term_i$ as being the $term_k$ that appears 
in the most documents:

```
BestHypernym(term_i) = term_k such that
    \forall term_j \in CandHypernym(term_i) :
        D(term_k) > D(term_j)
```

Removing this term $term_k$ from CandHypernym($term_i$) and repeating the heuristic allows to 
extract the most hypernyms candidates to the $term_i$.

@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('methods.inriasac')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Set standard output encoding to UTF-8.
from codecs import getwriter, open
sys.stdout = getwriter('UTF-8')(sys.stdout)

from structure.methods import MethodInterface
 
class INRIASAC(MethodInterface):
    """
    Identify hierarchical relations using the SLQS algorithm.
    """
    def __init__(self):
        MethodInterface.__init__(self)



