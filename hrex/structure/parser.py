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
    def __init__(self, extract='NounPhrases', mode='word'):
        """
        Initiate the elements of the class.
        
        Parameters:
        -----------
        extract : string {'WordsAndTags','Tree','Deps'}, optional
            specifies the type of content to be extracted
                WordsAndTags: returns the content from self.getPhrase()
                Tree: returns the content from self.getTree()
                Deps: returns the content from self.getDeps()
        mode : {'word', 'lemma'}, optional
            Specifies the mode of dealing with elements.
            word: words are extracted
            lemma: lemmas are extracted

        Notes:
        ------
        self.phrase: array_like
            retains each phrase of the corpus when iterating
        self.tree: array_like
            retains the parsed tree of the phrase when iterating
        self.deps: array_like
            retains the parsed dependencies of the phrase when iterating
        """ 
        self.extract = extract
        self.mode = mode
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
        Returns:
        --------
        self.phrase : array_like
            The content of self.phrase
        """
        return self.phrase


    def getTree(self):
        """
        Returns:
        --------
        self.tree : array_like
            The content of self.tree
        """
        return self.tree


    def getDeps(self):
        """
        Returns:
        --------
        self.deps : array_like
            The content of self.deps
        """
        return self.deps


    def _normalization(self, term):
        """
        Transform PoS tags from a term into its simplified version.

        Parameters:
        -----------
        pos : string
            String containing the PoS tag

        Returns:
        --------
        pos : string
            Returns the normalized form of the string (in case)

        Examples:
        ---------
        >>> Stanford()._normalization('NN')
            n
        >>> Stanford()._normalization('VBG')
            v
        """ 
        pass


    def _contentPos(self, pos, content='nvj'):
        """
        Verify wether a PoS tags belongs to a content word or not.

        Parameters:
        -----------
        pos : string
            String containing the PoS tag
        content : string {'nvjp', 'nvj', 'nv', 'n', 'vjp', ..., 'j'}
            A identifier to the content words to be extracted

        Returns:
        --------
        pos : boolean {True, False}
            True to a PoS that is from a content word, otherwise False

        Examples:
        ---------
        >>> Stanford()._contentPos('v', content='nvj')
            True
        >>> Stanford()._contentPos('DT', content='nvj')
            False
        """ 
        pass


    def listOfTerms(self, content_words=True, ctw='njv', normalize=True):
        """
        Transform the elements of the phrase into a list of nametuples.            

        Parameters:
        -----------
        content_words : boolean {True, False}, optional
            Remove non-content words from the phrase.
        ctw : string {'npjv', 'npj', 'np', 'nj', 'n', ..., 'j'}, optional 
            The content words that should be extracted by `content_words=True`, being:
                n = nouns
                p = pronouns
                j = adjectives
                v = verbs
        normalize : boolean {True|False}, optional
            calls self._normalization()

        Returns:
        --------
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
        Extract the noun phrases of the sentence.

        Returns:
        --------
        lnp : array_like
            List of all noun phrases in the sentence. Nestled noun phrases
            are also extracted. 

        Examples:
        --------
        >>> Parser().phrase = '(NP (NP (DT a) (NN game)) (PP (IN in) (NP (NN hand))))'
        >>> Parser().nounPhrases()
            [NP(id=1, np=[(DT a), (NN game)], head='game'),
             NP(id=2, np=[(NN hand)], head='hand'),
             NP(id=3, np=[(DT a), (NN game), (IN in), (NN hand)], head='game')
            ]
        """
        pass


    def plainPhrase(self):
        """
        Extract the conent of the phrase

        Returns:
        --------
        phrase : string
            Return a string with the plain text of the phrase. 
            The phrase does not contain the part of speech tags.

        Examples:
        ---------
        >>> Parser().phrase = 'The/DT newly/RB installed/VBN video/JJ
                                 surveillance/NNP system/NN ./.'
        >>> Parser().plainPhrase()
            'The newly installed video surveillance system .'
        """
        pass


    def contentWords(self, ctw='njvp'):
        """
        Extract content words of the phrase (i.e., words that contain
        some meaning such as nouns, proper nouns, verbs and adjectives.
        To extract content words, the phrase must be transformed by
        ``listOfTerms`` and normalized.

        Parameters:
        -----------
        ctw: string {'npjv', 'npj', 'np', 'nj', 'n', ..., 'j'}, optional 
            The content words that should be extracted, being:
                n = nouns
                p = pronouns
                j = adjectives
                v = verbs

        Returns:
        --------
        cwords = array_like
            Return a list containing only content words in self.phrase. 
            

        Examples:
        ---------
        >>> p=[(DT The), (RB newly), (v installed), 
               (j video), (n surveillance), (n system)]
        >>> Parser(p).contentWords(ctw='n')
            [(n surveillance), (n system)]
        """
        pass
#End of class ParserInterface


    




