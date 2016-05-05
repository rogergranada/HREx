#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains an abstract class to parsers. This class should be
inherited by classes that implement the extraction from files that are
parsed.

@author: granada
"""

class ParserInterface(object):
    """
    Interface to classes that extract content from parsed files.
    """
    def __init__(self, content='NounPhrases', mode='word', filetype='.parsed'):
        """
        Initiate the elements of the class.
        
        Parameters:
        -----------
        content: specifies the type of content to be extracted
            NounPhrases: returns the content from self.nounPhrases()
            PlainPhrase: return the content from self.plainPhrase()
            ListOfTerms: returns the content from self.listOfTerms()
            ContentWords: returns the content from self.contentWords()
        mode: specifies the mode of deal with elements
        mode : {'reduced', 'complete', 'r', 'raw', 'full', 'economic'}, optional
            word: words are extracted
            lemma: lemmas are extracted
        filetype: the extension of the accepted files (e.g. .xml, .parsed)

        Notes:
        ------
        self.phrase: retains each phrase of the corpus when iterating
        self.tree: retains the parsed tree of the phrase when iterating
        self.deps: retains the parsed dependencies of the phrase when iterating
        """ 
        self.mode = mode
        self.filetype = filetype
        self.phrase = ''
        self.tree = ''
        self.deps = []


    def __iter__(self):
        """
        Iterate over the corpus yielding a phrase at time.
        It depends on the self.mode to yield the content. Thus, in case of
            `mode=words`: __iter__ should yield the words of the phrase
        """
        pass


    def getPhrase(self):
        """
        Returns
        -------
        self.phrase : array_like
            The content of self.phrase
        """
        return self.phrase


    def getTree(self):
        """
        Returns
        -------
        self.tree : array_like
            The content of self.tree
        """
        return self.tree


    def getDeps(self):
        """
        Returns
        -------
        self.deps : array_like
            The content of self.deps
        """
        return self.deps


    def _normalization(self, term):
        """
        Transform PoS tags from self.phrase into its simplified version.
            Original tags: ['NN', 'NNS', 'NNP', 'NNPS']
            Normalized: ['n']
            Original tags: ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
            Normalized: ['v']

        Parameters:
        -----------
        term : namedtuple
            Namedtuple containing the word and PoS tag as:
            Term(word=u'Minute', pos=u'NN')

        Returns
        -------
        phrase : namedtuple
            Namedtuple containing the word and PoS normalized as:
            Term(word=u'Minute', pos=u'n')
        """ 
        pass


    def listOfTerms(self, content_words=True, ctw='njv', normalize=True):
        """
        Transform the elements of the phrase into a list of nametuples.            

        Parameters:
        -----------
        content_words : string 
            Remove non-content words from the phrase.
        ctw : string 
            The content words that should be extracted by `content_words=True`, being:
                n = nouns
                p = pronouns
                j = adjectives
                v = verbs
        normalize : binary {True|False}
            calls self._normalization()

        Returns
        -------
        phrase : array_like
            Return namedtuple objects containing elements of the phrase
                [Term(word=u'Minute', pos=u'JJ'),
                Term(word=u'bubbles', pos=u'NNS'),
                Term(word=u'of', pos=u'IN'),
                Term(word=u'ancient', pos=u'JJ'),
                Term(word=u'air', pos=u'NN')]
            where `Term` is a `namedtuple('Term', ['word', 'pos'])`
        """
        pass


    def nounPhrases(self):
        """
        Return all the noun phrases of the phrase. Nestled noun phrases should
        also be extracted. Thus, the content of:
            (NP (NP (DT a) (NN game)) (PP (IN in) (NP (NN hand))))
        should be extracted as:
            [NP(id=1, np='a game', head='game'),
             NP(id=2, np='hand', head='hand'),
             NP(id=3, np='a game in hand', head='game')
            ]
        where NP is a `namedtuple('NP', ['id', 'np', 'head'])`
        """
        pass


    def plainPhrase(self):
        """
        Return a string with the plain text of the phrase. 
        The phrase does not contain the part of speech tags.
        E.g. the phrase: [(DT The), (RB newly), (VBN installed), 
                          (JJ video), (NNP surveillance), (NN system)]
        Returns: 'The newly installed video surveillance system'
        """
        pass


    def contentWords(self, ctw='njvp'):
        """
        Return a list containing only content words in self.phrase. 
        ctw: The content words that should be extracted, being:
            n = nouns
            p = pronouns
            j = adjectives
            v = verbs

        For an input in the form:
            [(DT The), (RB newly), (VBN installed), (JJ video), (NNP surveillance), (NN system)]
        The output list has the form of:
            [(VBN installed), (JJ video), (NNP surveillance), (NN system)]
        """
        pass
#End of class ParserInterface


    




