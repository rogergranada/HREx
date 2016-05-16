#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains classes that implement many types of dictionaries.
It is easier to create a classes for setting auto increment or append
content in lists than do it manually in each code. 

@author: granada
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger('structure.dictionaries')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from collections import defaultdict

from storage import SQLite, Shelve, PlainText

import operator
from collections import Counter
from codecs import open
from os.path import join


class DictList(dict):
    """
    Dictionary that append elements for each key.
    The dictionary has the form:
        
    dict: {key: [value_1, value_2, ...]}
    """
    def __init__(self, input=None, dname=None):
        """
        Initiate an empty dictionary or load an existing dictionary 
        from a plain text file, shelve, database (sqlite3) or from 
        another dictionary.

        input: string (name of the file or database)
        dname: name of the stored dictionary
        """
        if isinstance(input, basestring):
            super(DictList, self).__init__()
            self.load_from_text(input)
        elif isinstance(input, SQLite):
            super(DictList, self).__init__()
            self.load_from_db(input, dic=dname)
        elif isinstance(input, Shelve):
            self.load_from_shelve(input, dic=dname)
        else:
            super(DictList, self).__init__()


    def __setitem__(self, key, value):
        """
        Set item and add value to an array of values.

        key: key of the dictionary
        value: value that is appended 
        """
        if value:
            if dict.has_key(self, key):
                ar = dict.__getitem__(self, key)
                if isinstance(value, list):
                    ar.extend(value)
                else:
                    ar.append(value)
                dict.__setitem__(self, key, ar)
            else:
                if isinstance(value, list):
                    dict.__setitem__(self, key, value)
                else:
                    dict.__setitem__(self, key, [value])


    def __getitem__(self, key):
        """
        Return the list containing the key.
        """
        return dict.__getitem__(self, key)


    def load_from_text(self, fname):
        """
        Load a dictionary with lists from plain text files. The
        file contains the format:
            key element_1
            key element_2
            ...

        fname: name of the file containing the dictionary
        """
        logger.info('loading dictionary from file: %s' % fname)
        with open(fname, 'r', 'utf-8') as fin:
            for line in fin:
                k, v = line.strip().split()
                self.__setitem__(k, v)

    
    def load_from_db(self, input, dic=None):
        """
        Load a dictionary with lists from SQLite database.

        dic: name of the table containing the dictionary
        """
        logger.info('loading dictionary: %s' % dic)
        #TODO


    def load_from_shelve(self, db, dic=None):
        """
        Load a dictionary stored in a shelved file.
        """
        logger.info('loading dictionary: %s' % dbname)
        db = shelve.open(fname)
        dict.__init__(self, DictList(db[dic]))
#End of class DictList


class AbstractDictionary(dict):
    """
    Class to implement shared functions
    """
    def __init__(self, input=None):
        """
        Initiate the class SQLite.

        Parameters:
        -----------
        input : string, optional
            A dictionary that is transformed into DictWords
        """
        self.dict_t = {}
        if input:
            dict.__init__(self, input)
        else:
            dict.__init__(self)


    def id2key(self, simplify=False):
        """
        Invert the dictionary, transforming the key into id and 
        the id into key.

        Parameters:
        -----------
        simplify : boolean {True, False}, optional
            Return a instance of `dict` instead of an instance
            of the class

        Returns:
        --------
        self.dic_t : dict or DictWords instance
            The dictionary containing the id as key and the word 
            as value.

        **This method must be implemented by each class**
        """
        pass


    def simplify(self, transposed=False):
        """
        Simplify transforms each namedtuple into a normal tuple.

        Parameters:
        -----------
        transposed : boolean {True, False}, optional
            Transform keys into ids and ids into keys

        Returns:
        --------
        intance of dict
            Dictionary of inverse dictionary

        Examples:
        ---------
        >>> d = DictWords({'w1': (1,1), 'w2':(2,4), 'w3':(3,5)})
        >>> isinstance(d.simplify(), dict)
            True
        >>> d.simplify(transposed=True)
            {1: ('w1',1), 2:('w2',4), 3:('w3',5)}

        >>> d = DictRels({(1,2): 1, (1,3): 2, (2,3): 3})
        >>> isinstance(d.simplify(), dict)
            True
        >>> d.simplify(transposed=True)
            {(2, 1): 1, (3, 1): 2, (3, 2): 3}
        """
        if transposed:
            return dict(self.id2key())
        else:
            return dict(self.copy())


    def save(self, fout, dname=None, mode='db', new=False):
        """
        Save the dictionary into `fout`.

        Parameters:
        -----------
        fout : string
            The path to the output file
        dname : string {'dwords','dctxs', 'drels'}
            The name of the dictionary
        mode : string {'text', 'db', 'shelve'}
        """
        if mode == 'db':
            dbm = SQLite(fout)
        elif mode == 'shelve':
            dbm = Shelve(fout)
            if new:
                dbm.clear()
        elif mode == 'text':
            ftxt = PlainText(fout)
            comm = '%%word id frequency'
            ftxt.save(self, dtype=dname, transposed=False)
            return True
        else:
            logger.error('Cannot save dictionary - `mode=%s` no specified' % mode)
            return False
        dbm.save(self, dtype=dname)
        dbm.close()
        return True


    def load(self, fin, dname=None, mode='db'):
        """
        Load the dictionary from `fin`.

        Parameters:
        -----------
        fin : string
            The path to the input file
        dname : string {'dwords','dctxs', 'drels'}
            The name of the dictionary
        mode : string {'text', 'db', 'shelve'}
        """
        if mode == 'db':
            dbm = SQLite(fin)
        elif mode == 'shelve':
            dbm = Shelve(fin)
        elif mode == 'text':
            dbm = PlainText(fin)
            dic = dbm.load(dtype=dname, transposed=False)
            dict.__init__(self, dic)
            dbm.close()
            return True
        else:
            logger.error('Cannot load dictionary - `mode=%s` no specified' % mode)
            return False
        dic = dbm.load(self, dtype=dname)
        dict.__init__(self, dic)
        dbm.close()
        return True

    def stats(self):
        """
        Print stats about the dictionary.
        """
        logger.info('dictionary conaining %d terms' % len(dict.keys(self)))
#End of AbstractDictionary


class DictWords(AbstractDictionary):
    """
    DicWords is a dictionary for words and contexts. It contains the ID 
    and the frequency of each word. It has the form:
        [word]: (id, freq)
    """
    def __init__(self, input=None):
        """
        Initiate the class SQLite.

        Parameters:
        -----------
        input : string, optional
            A dictionary that is transformed into DictWords
        """
        if input:
            AbstractDictionary.__init__(self, input=input)
        else:
            AbstractDictionary.__init__(self, input=input)
            self.id = 1


    def __setitem__(self, key, value):
        """
        Add element to the dictionary. The frequency is summed up 
        each time the same word is added.

        Parameters:
        -----------
        key : string, int
            The key of the dictionary
        value: int, string, tuple
            Values to be added to the key value

        Examples:
        ---------
        >>> d = DictWords()
        >>> d['w1'] = 3
            {'w1': (1, 3)}
        >>> d['w1'] = 4
            {'w1': (1, 7)}
        """
        if isinstance(value, tuple):
            id, freq = value
            if dict.has_key(self, key):
                id, f = dict.__getitem__(self, key)
                dict.__setitem__(self, key, (id, f+freq))
            else:
                dict.__setitem__(self, key, (id, freq))
        else:
            if dict.has_key(self, key):
                id, f = dict.__getitem__(self, key)
                dict.__setitem__(self, key, (id, f+value))
            else:
                dict.__setitem__(self, key, (self.id, value))
                self.id += 1


    def id2key(self, simplify=False):
        """
        Invert the dictionary, transforming the key into id and 
        the id into key.

        Parameters:
        -----------
        simplify : boolean {True, False}, optional
            Return a instance of `dict` instead of an instance
            of the class

        Returns:
        --------
        self.dic_t : dict or DictWords instance
            The dictionary containing the id as key and the word 
            as value.
        """
        if not self.dict_t:
            self.dict_t = DictWords()
            for key in dict.iterkeys(self):
                t, f = dict.__getitem__(self, key)
                self.dict_t[t] = (key, f)
        if simplify:
            return self.dict_t.simplify()
        else:
            return self.dict_t


    def dic2Tuples(self, key='id'):
        """
        Return the dictionary in form of tuples.

        Parameters:
        -----------
        key : string {'id', 'word'}
            Define the element to be the key (first element of the
            tuple).
        
        Returns:
        --------
        ld = array_like
            A list containing all tuples from the dictionary

        Examples:
        ---------
        >>> d = DictWords({'w1': (1,1), 'w2':(2,4), 'w3':(3,5)})
        >>> d.dic2Tuples(key='id')
            [(1, 'w1', 1),(2, 'w2', 4),(3, 'w3', 5)]
        >>> d.dic2Tuples(key='word')
            [('w1', 1, 1),('w2', 2, 4),('w3', 3, 5)]
        """
        if key not in ['id', 'word']:
            logger.error('there is no such key in the dictionary: %s' % key)
            return False

        tuples = []
        for w in dict.iterkeys(self):
            t, f = dict.__getitem__(self, w)
            if key == 'id':
                tuples.append((t, w, f))
            elif key == 'word':
                tuples.append((w, t, f))
        return tuples


    def has_id(self, id):
        """
        Verify wether the dictionary contains the id.
        
        Parameters:
        -----------
        id : integer
            Id in the dictionary
        """
        if not self.dict_t:
            self.id2key()
        return self.dict_t.has_key(id)


    def setId(self, key, newid):
        """
        Change the key in the dictionary from id to the new id.

        Parameters:
        -----------
        key : int, string
            The key of the dictionary
        newid : int, string
            The new key that will substitute
        """ 
        if dict.has_key(self, key):
            id, f = dict.__getitem__(self, key)
            dict.__setitem__(self, key, (newid, f))
        else:
            logger.error('there is no such key in the dictionary: %s' % key)


    def setFreq(self, key, newf):
        """
        Change the value of the `freq` for a certain key. 
        This is used to update the dictionary, changing the 
        values of frequency to values of entropy.

        Parameters:
        -----------
        key : int, string
            The key of the dictionary
        newf : int, float
            The new value for the frequency column
        """
        if dict.has_key(self, key):
            id, f = dict.__getitem__(self, key)
            dict.__setitem__(self, key, (id, newf))
        else:
            logger.error('there is no such key in the dictionary: %s' % key)


    def getFreq(self, key, transposed=False):
        """
        Return the frequency of a certain key. `key` has the
        value of `word` in case of `transposed=False` and the
        value of `id` in case of `transposed=True`.

        Parameters:
        -----------
        transposed : boolean {True, False}, optional
            Transform keys into ids and ids into keys

        Returns:
        --------
        The frequency of the key
        """
        if transposed:
            self.id2key()
            if self.dict_t.has_key(key):
                v, f = dict_t[key]
            else:
                f = None
        else:
            if dict.has_key(self, key):
                v, f = dict.__getitem__(self, key)
            else:
                f = None
        return f
#End of class DictWords


class DictRels(AbstractDictionary):
    """
    DictRels is a dictionary for store relations betweeen words and contexts. 
    It contains the ID of the word, the ID of the context and the frequency
    of the occurrence of both. It has the form:
        (idw, idc): freq
    """
    def __init__(self, input=None):
        """
        Initiate the class SQLite.

        Parameters:
        -----------
        input : string, optional
            A dictionary that is transformed into DictWords
        """
        AbstractDictionary.__init__(self, input=input)


    def __setitem__(self, key, value):
        """
        Add element to the dictionary. The frequency is summed up 
        each time the same key is added.

        Parameters:
        -----------
        key : tuple
            A pair of ids (idw, idc)
        value: int
            The frequency of the pair key

        Examples:
        ---------
        >>> d = DictRels()
        >>> d[(1, 2)] = 1
            {(1, 2): 1}
        >>> d[(1, 2)] = 4
            {(1, 2): 5}
        """
        if dict.has_key(self, key):
            f = dict.__getitem__(self, key)
            dict.__setitem__(self, key, f+value)
        else:
            dict.__setitem__(self, key, value)


    def id2key(self, simplify=False):
        """
        Invert the dictionary, transforming the first key into 
        the second and vice versa.

        Parameters:
        -----------
        simplify : boolean {True, False}, optional
            Return a instance of `dict` instead of an instance
            of the class

        Returns:
        --------
        self.dic_t : dict or DictRels instance
            The dictionary containing the id as key and the word 
            as value.
        """
        if not self.dict_t:
            self.dict_t = DicRels()
            for key in dict.iterkeys(self):
                idw, idc = key
                f = dict.__getitem__(self, key)
                self.dict_t[(idc, idw)] = f
        if simplify:
            return self.dict_t.simplify()
        else:
            return self.dict_t


    def dic2Tuples(self, key='idw', transposed=False):
        """
        Return the dictionary in form of tuples.

        Parameters:
        -----------
        key : string {'idw', 'idc'}
            Choose the element to be the first element of the tuple
        transposed : boolean {True, False}, optional
            Transform keys into ids and ids into keys

        Returns:
        --------
        ld = array_like
            A list containing all tuples from the dictionary

        Notes:
        ------
        Using `key='idc'` is equal to use transposed=True

        Examples:
        ---------
        >>> d = DictRels({(1,2): 1, (1,3): 2, (2,3): 3})
        >>> d.dic2Tuples(transposed=False)
            [(1, 2, 1),(1, 3, 2),(2, 3, 3)]
        >>> d.dic2Tuples(transposed=True)
            [(2, 1, 1),(3, 1, 2),(3, 2, 3)]
        """
        tuples = []
        for key in dict.iterkeys(self):
            idw, idc = key
            f = dict.__getitem__(self, key)
            if transposed or id == 'idc':
                tuples.append((idc, idw, f))
            else:
                tuples.append((idw, idc, f))
        return tuples


    def setFreq(self, key, newf):
        """
        Change the value of the `freq` for a certain key. 

        Parameters:
        -----------
        key : int, string
            The key of the dictionary
        newf : int, float
            The new value for the frequency
        """
        if dict.has_key(self, key):
            dict.__setitem__(self, key, newf)
        else:
            logger.error('there is no such key in the dictionary: %r' % key)


    def getFreq(self, key):
        """
        Return the frequency of a certain key.
        """
        return self.__getitem__(key)


    def getContexts(self, key):
        """
        Return a list of contexts to a certain `key`.
        
        Parameters:
        -----------
        key : int
            The id of the word to get the contexts.

        Returns:
        --------
        contexts : list
            A list containing all contexts of `key`
        """
        contexts = []
        for k in dict.iterkeys(self):
            idw, idc = k
            if idw == key:
                contexts.append(idc)
        return contexts

#End of class DictWords
