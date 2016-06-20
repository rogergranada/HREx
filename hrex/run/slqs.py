#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module runs the file `methods.slqs`

@author: granada
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger('run.slqs')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from corpus.corpus import Corpus
from corpus import filters
from methods import slqs
from resources.wordnet import WordNet
from structure.parameters import Parameters


def main(argv):
    # load parameters from command line
    p = Parameters(argv)

    # load DF class to get the default settings
    method = slqs.SLQS()
    dset = method.defaultSettings()

    # load corpus into Corpus class and load `corpus.dwords` with a window of size=5
    # values of `extractWindow` may be modified manually, but to facilitate here we
    # are using the default values load from `slqs.defaultSettings()`
    corpus = Corpus(p.inputfile(), lang='en', parser='Stanford', filetype='.parsed')
    corpus.extractWindow(size=dset.window, lex_mode=dset.lex_mode, cwords=dset.cwords, 
                         ctw=dset.ctw, normalize=dset.normalize, lower=dset.lower)

    # weight relations using Local Mutual Information (LMI)
    # replace=True changes the values of corpus.drels to the LMI values
    corpus.weightRels(measure='lmi', replace=True)

    # filter the dictionary of words keeping only words that appear in WordNet
    wn = WordNet()
    dwn = wn.filterDictionary(dic=corpus.dwords)

    # filter the dictionary from WordNet keeping only the top 10 most frequent terms
    dtopN = filters.filter_topN(dwn, N=10)

    # save the dictionary in a text file
    dtopN.save(p.outputfile(), dtype='dwords', mode='text', new=True)

    # filter out non related contexts and set the `corpus.drels` to the limited
    # word by context matrix
    dfiltered = filters.filterTopNContexts(corpus.drels, N=5)
    corpus.setDrels(dfiltered)

    # calculate the entropy of each context, `replace=True` set the values of
    # `corpus.dctxs` to the values of entropy. `normalize=True` applies min-max
    # scaling on the contexts values 
    corpus.weightContexts(measure='entropy', replace=True, normalize=True)

    # load SLQS class with the topN dictionary and identify relations between words
    # the contexts with their value of entropy and the relations between words and
    # contexts
    method = slqs.SLQS(dtopN, corpus.dctxs, corpus.drels)
    method.identifyRelations()

    # save relations into a file
    method.save(p.outputfile())

    # print Precision, Recall and F-measure based on WordNet
    logger.info('precision: %f' % method.precision(WordNet))
    logger.info('recall: %f' % method.recall(WordNet))
    logger.info('f-measure: %f' % method.fmeasure(WordNet))
    

if __name__ == "__main__":
   main(sys.argv[1:])
