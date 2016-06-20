#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module runs the file `methods.inriasac`

@author: granada
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger('run.inriasac')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from corpus.corpus import Corpus
from corpus import filters
from methods import inriasac
from resources.wordnet import WordNet
from structure.parameters import Parameters


def main(argv):
    # load parameters from command line
    p = Parameters(argv)

    # load DF class to get the default settings
    method = inriasac.INRIASAC()
    dset = method.defaultSettings()

    # load corpus into Corpus class and load `corpus.dwords` with `df`
    corpus = Corpus(p.inputfile(), lang='en', parser='Stanford', filetype='.parsed')
    corpus.extractSentences(dset.lex_mode, dset.cwords, dset.ctw, dset.normalize, dset.lower)

    # filter the dictionary of words keeping only words that appear in WordNet
    wn = WordNet()
    dwn = wn.filterDictionary(dic=corpus.dwords)

    # filter the dictionary from WordNet keeping only the top 10 most frequent terms
    dtopN = filters.filter_topN(dwn, N=10)

    # save the dictionary in a text file
    dtopN.save(p.outputfile(), dtype='dwords', mode='text', new=True)
    corpus.drels.save(p.outputfile(), dtype='drels', mode='text', new=True)

    # load DF class with the topN dictionary and identify relations between words
    method = inriasac.INRIASAC(dtopN, corpus.drels)
    method.identifyRelations()

    # save relations into a file
    method.save(p.outputfile())

    # print Precision, Recall and F-measure based on WordNet
    logger.info('precision: %f' % method.precision(WordNet))
    logger.info('recall: %f' % method.recall(WordNet))
    logger.info('f-measure: %f' % method.fmeasure(WordNet))
    

if __name__ == "__main__":
   main(sys.argv[1:])
