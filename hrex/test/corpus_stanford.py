#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module tests the file `corpus.stanford`

@author: granada
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger('test.corpus_stanford')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from corpus import stanford

from codecs import open
from os.path import join

def test_load():
    HOME='/home/roger/Desktop/tests/footie.parsed'
    parsed = stanford.Stanford(HOME, extract='WordsAndTags')
    for k in parsed:
        if not k:
            raise 'Error WordsAndTags'
        elif not parsed.listOfTerms(content_words=False, normalize=True):
            raise 'Error listOfTerms()'
        elif not parsed.listOfTerms(content_words=True, ctw='njv', normalize=True):
            raise 'Error listOfTerms()'
        elif not parsed.listOfTerms(content_words=True, ctw='njv', normalize=False):
            raise 'Error listOfTerms()'
        elif not parsed.nounPhrases():
            raise 'Error nounPhrases()'
        elif not parsed.plainPhrase():
            raise 'Error plainPhrase()'
        elif not parsed.contentWords(ctw='njv'):
            raise 'Error contentWords()'
        try:
            parsed.contentWords(ctw='')
            raise 'Error contentWords()'
        except:
            pass
        break

    parsed = stanford.Stanford(HOME, extract='Tree')
    for k in parsed:
        if not k:
            raise 'Error Tree'
        break

    parsed = stanford.Stanford(HOME, extract='Deps')
    for k in parsed:
        if not k:
            raise 'Error Deps'
        break
        
    print 'Finished!'
 
if __name__ == "__main__":
    test_load()
