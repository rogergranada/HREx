#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains a parsing to Stanford files.
@author: granada
""" 

import os
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('corpus.stanford')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from codecs import open
from collections import namedtuple
NP = namedtuple('NP', ['id', 'np', 'head'])
Term = namedtuple('Term', ['word', 'pos'])

try:
    import nltk
    hasNLTK = True
except ImportError:
    hasNLTK = False

from structure.parser import ParserInterface 

class Stanford(ParserInterface):
    """
    Class that deals with texts parsed by Stanford parser.
    """
    def __init__(self, input, extract='WordsAndTags', mode='word'):
        """
        Initiate the elements of the class.
        
        Parameters:
        -----------
        input : string
            This parameter must be a basestring type and the content of the
            file must be parsed with the option:
                ``-outputFormat "penn,wordsAndTags,typedDependenciesCollapsed"`` 
        extract : string {'WordsAndTags','Tree','Deps'}, optional
            specifies the type of content to be extracted
                WordsAndTags: returns the content from self.phrase
                Tree: returns the content from self.tree
                Deps: returns the content from self.deps
        mode : {'word', 'lemma'}, optional
            Specifies the mode of dealing with elements.
            word: words are extracted
            lemma: lemmas are extracted

        Notes:
        ------
        self.phrase: string
            retains each phrase of the corpus when iterating
        self.tree: string
            retains the parsed tree of the phrase when iterating
        self.deps: array_like
            retains the parsed dependencies of the phrase when iterating
        """ 
        ParserInterface.__init__(self, extract=extract, mode=mode)
        self.fin = open(input, 'r', 'utf-8')
        self.extract = extract
        self.phrase = ''
        self.tree = ''
        self.deps = []

    def __iter__(self):
        """
        Iterate over the corpus yielding a phrase at time.
        It depends on the self.mode to yield the content. Thus, in case of
            `mode=words`: __iter__ should yield the words of the phrase
        """
        pos = True     #semaphore : PoS part of the text
        parsed = False #semaphore : parsed tree
        dep = False    #semaphore : dependencies of the phrase

        logger.info('Reading lines from corpus')
        #pb = ProgressBar(self.__len__())
        for n, line in enumerate(self.fin):
            #print line
            line = line.strip()
            if line == '':
                if pos: 
                    # after loading PHRASE
                    parsed = True
                    pos = False
                elif parsed: 
                    # after loading TREE
                    dep = True
                    parsed = False
                elif dep: 
                    # after loading DEPENDENCIES
                    pos = True
                    dep = False
                    

                    # yield elements
                    if self.extract == 'WordsAndTags':
                        yield self.phrase
                    elif self.extract == 'Tree':
                        yield self.tree
                    elif self.extract == 'Deps':
                        yield self.deps
                    else:
                        yield (self.phrase, self.tree, self.deps)

                    self.phrase = ''
                    self.tree = ''
                    self.deps = []
            else:
                if pos:
                    self.phrase = line
                elif parsed:
                    self.tree += line+' '
                elif dep:      
                    self.deps.append(line)
            #pb.update()


    def _normalization(self, pos):
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
        ctw_N = ['NN', 'NNS', 'NNP', 'NNPS']
        ctw_P = ['PRP', 'PRP$']
        ctw_J = ['JJ']
        ctw_V = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        if pos in ctw_N : return 'n'
        elif pos in ctw_P : return 'p'
        elif pos in ctw_J : return 'j'
        elif pos in ctw_V : return 'v'
        return pos


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
        ctw_N = ['NN', 'NNS', 'NNP', 'NNPS', 'n']
        ctw_J = ['JJ', 'j']
        ctw_V = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'v']
        if   'n' in content and pos in ctw_N: return True
        elif 'j' in content and pos in ctw_J: return True
        elif 'v' in content and pos in ctw_V: return True
        return False


    def listOfTerms(self, content_words=True, ctw='njv', normalize=True, lower=False):
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
        normalize : boolean {True, False}, optional
            calls self._normalization()
        lower : boolean {True, False}, optional
            Transform word to lowecase

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
        sent = []
        for term in self.phrase.split():
            ar = term.split('/')
            if len(ar) == 2:
                word = ar[0]
            else:
                word = '/'.join(ar[:-1])
            if lower:
                word = word.lower()
            pos = ar[-1]
            if normalize:
                pos = self._normalization(pos)

            if content_words:
                if self._contentPos(pos, content=ctw):
                    sent.append(Term(word, pos))
            else:
                sent.append(Term(word, pos))
        return sent


    def _treeToNP(self, tree):
        """ 
        Recursively extracts NPs from a parsed (chunked) tree.

        Parameters:
        -----------
        tree : NLTK.tree.Tree instance
            Tree format generated by NLTK

        Returns:
        --------
        lnp : array_like
            List containing all noun phrases generated by the tree
        """
        lnp = []
        if (tree.label() == 'NP'):
            lnp.append(tree.copy(True))
        for child in tree:
            if (type(child) is nltk.Tree):
                inner_lnp = self._treeToNP(child)
                if (len(inner_lnp) > 0):
                    lnp.extend(inner_lnp)
        return lnp


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
        >>> Stanford().tree = '(NP (NP (DT a) (NN game)) (PP (IN in) (NP (NN hand))))'
        >>> Stanford().nounPhrases()
            [NP(id=1, np=[(DT a), (NN game)], head='game'),
             NP(id=2, np=[(NN hand)], head='hand'),
             NP(id=3, np=[(DT a), (NN game), (IN in), (NN hand)], head='game')
            ]
        """
        if hasNLTK:
            parsed_tree = nltk.tree.Tree.fromstring(self.tree[0:-1])
            subtrees = self._treeToNP(parsed_tree)

            lnp = []
            id = 0
            for subtree in subtrees:
                np = []
                for word, pos in subtree.pos():
                    np.append(Term(word, pos))
                lnp.append(NP(id=id, np=np, head=''))
        else:
            raise 'NLTK tool not installed to extract Noun Phrases'
        return lnp


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
        >>> Stanford().phrase = 'The/DT newly/RB installed/VBN video/JJ
                                 surveillance/NNP system/NN ./.'
        >>> Stanford().plainPhrase()
            'The newly installed video surveillance system .'
        """
        sent = ''
        for el in self.phrase.split():
            ar = el.split('/')
            if len(ar) == 2:
                sent += ar[0]+' '
            else:
                sent += '/'.join(ar[:-1])+' '
        return sent[:-1]


    def contentWords(self, ctw='njv'):
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
            
        Raises:
        -------
        ValueError
            In case `ctw` does not contain any value

        Examples:
        ---------
        >>> p=[(DT The), (RB newly), (v installed), 
               (j video), (n surveillance), (n system)]
        >>> Parser(p).contentWords(ctw='n')
            [(n surveillance), (n system)]
        """
        if not ctw:
            raise ValueError, 'a content word must be passed as argument'
        return self.listOfTerms(content_words=True, ctw=ctw, normalize=True)


    def document(self, content_words=True, ctw='njv', normalize=True, lower=False):
        """
        Extracts the whole document as a list of terms. No sentence border is
        added. This should be used when extracting a window using small documents.

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
        lower : boolean {True, False}, optional
            Transform word to lowecase

        Returns:
        --------
        document : array_like
            Return namedtuple objects containing all elements of the document
                [Term(word=u'Minute', pos=u'JJ'),
                Term(word=u'bubbles', pos=u'NNS'),
                Term(word=u'of', pos=u'IN'),
                Term(word=u'ancient', pos=u'JJ'),
                Term(word=u'air', pos=u'NN')]
            where `Term` is a `namedtuple('Term', ['word', 'pos'])`
        """
        doc = []
        for _ in self.__iter__():
            doc.extend(self.listOfTerms(content_words, ctw, normalize, lower))
        return doc
