#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains util functions that may be used by other modules.

@author: granada
"""
import logging
logger = logging.getLogger('utils.mathutils')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np

def pmi(n_ii, n_ix, n_xi, n_xx):
    """
    Calculate the Pontwise Mutual Information such as:
        $PMI(w,c) = log_2 \left ( \frac{P(w|c)}{P(w)P(c)} \right )$

    Parameters:
    -----------
                w1    ~w1
         ------ ------
         w2 | n_ii | n_oi | = n_xi
         ------ ------
        ~w2 | n_io | n_oo |
         ------ ------
             = n_ix        TOTAL = n_xx

        n_xx = n_ii + n_oi + n_io + n_oo

    Notes:
    ------
        pwc = n_ii / float(n_xx)
        pw = n_ix / float(n_xx)
        pc = n_xi / float(n_xx)
        pmi = np.log2(pwc/(float(pw * pc))
    """
    p_wc = n_ii / float(n_xx)
    pmi = (np.log2((n_ii * n_xx) / float(n_ix * n_xi)))
    return pmi


def ppmi(n_ii, n_ix, n_xi, n_xx):
    """
    Calculate Positive Pontwise Mutual Information (PPMI), i.e.,
    the PMI where negative values become zero.

    Parameters:
    -----------
                w1    ~w1
         ------ ------
         w2 | n_ii | n_oi | = n_xi
         ------ ------
        ~w2 | n_io | n_oo |
         ------ ------
             = n_ix        TOTAL = n_xx

        n_xx = n_ii + n_oi + n_io + n_oo
    """
    vpmi = pmi(n_ii, n_ix, n_xi, n_xx)
    if vpmi < 0:
        vpmi = 0
    return vpmi


def lmi(n_ii, n_ix, n_xi, n_xx):
    """
    Calculate the Local Mutual Information such as:
        $LMI(w,c) = P(w|c) * log_2 \left ( \frac{P(w|c)}{P(w)P(c)} \right )$

    Parameters:
    -----------
                w1    ~w1
         ------ ------
         w2 | n_ii | n_oi | = n_xi
         ------ ------
        ~w2 | n_io | n_oo |
         ------ ------
             = n_ix        TOTAL = n_xx

        n_xx = n_ii + n_oi + n_io + n_oo

    Notes:
    ------
        p_wc = n_ii / float(n_xx)
        pw = n_ix / float(n_xx)
        pc = n_xi / float(n_xx)
        pmi = np.log2(pwc/(float(pw * pc))
        lmi = p_wc * pmi
    """
    p_wc = n_ii / float(n_xx)
    pmi = (np.log2((n_ii * n_xx) / float(n_ix * n_xi)))
    return (p_wc * pmi)
