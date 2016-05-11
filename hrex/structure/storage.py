#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains classes that implement storage functions such
as databases. This serves as interface to interact with the database 
in terms of inclusion, exclusion, queries etc.

@author: granada
"""
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments
import logging
logger = logging.getLogger('corpus.databases')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import sqlite3 as lite
import shelve
from codecs import open
from os.path import basename

class SQLite(object):
    """
    Class that interact with SQLite3 database.
    """
    def __init__(self, dbname):
        """
        Initiate the class SQLite.

        Parameters:
        -----------
        dbname : string
            Location of the database
        """
        try:
            self.con = lite.connect(dbname)
        except lite.Error, e:
            logger.error('%s:' % e.args[0])
            sys.exit(1)


    def clear(self):
        """
        Clear dictionaries stored into the shelve.
        """
        cur = self.con.cursor()
        tables = list(cur.execute("SELECT name FROM sqlite_master WHERE type IS 'table'"))
        cur.executescript(';'.join(["drop table if exists %s" %i for i in tables]))


    def _createTable(self, table):
        """
        Create a new table in the database to a dictionary

        Parameters:
        -----------
        table : string {'dwords', 'dctxs', 'drels'}
            Type of table to be created
        """
        cur = self.con.cursor()
        if table == 'dwords':
            cur.execute('DROP TABLE IF EXISTS dwords')
            self.con.commit()
            newTable = """CREATE TABLE dwords(
                            idw INTEGER PRIMARY KEY, 
                            word TEXT, 
                            freq INTEGER
                          );"""
        elif table == 'dctxs':
            cur.execute('DROP TABLE IF EXISTS dctxs')
            self.con.commit()
            newTable = """CREATE TABLE dctxs(
                            idc INTEGER PRIMARY KEY, 
                            context TEXT, 
                            freq INTEGER
                          );"""
        elif table == 'drels':
            cur.execute('DROP TABLE IF EXISTS drels')
            self.con.commit()
            newTable = """CREATE TABLE drels(
                            idw INTEGER, 
                            idc INTEGER, 
                            freq INTEGER, 
                            FOREIGN KEY (idw) REFERENCES dwords(idw),
                            FOREIGN KEY (idc) REFERENCES dwords(idc),
                            PRIMARY KEY (idc, idw)
                          );"""
        else:
            logger.error('Cannot create table of type %d' % table)
            return False
        cur.execute(newTable)
        self.con.commit()
        return True


    def save(self, dic, dtype='dwords', new=True):
        """
        Save the content of a dictionary `dic`

        Parameters:
        -----------
        dic : {DictWords, DictRels} instance
            The dictionary to be saved
        dtype : string {'dwords', 'dctxs', 'drels'}
            The type of dictionary to be saved
        new : Boolean {True, False}, optional
            Create a new table to the dictionary
        """
        if new:
            self._createTable(dtype)
        cursor = self.con.cursor()
        elem = dic.dic2Tuples(key='id')
        if dtype == 'dwords':
            cursor.executemany('INSERT INTO dwords (idw, word, freq) VALUES (?,?,?)', elem)
        elif dtype == 'dctxs':
            cursor.executemany('INSERT INTO dctxs (idc, context, freq) VALUES (?,?,?)', elem)
        elif dtype == 'drels':
            cursor.executemany('INSERT INTO drels (idw, idc, freq) VALUES (?,?,?)', elem)
        else:
            logger.error('Cannot save dictionary of type %d' % dtype)
            return False
        self.con.commit()
        return True


    def load(self, dtype='dwords'):
        """
        Load the content of a dictionary `dic`

        Parameters:
        -----------
        dtype : string {'dwords', 'dctxs', 'drels'}
            The type of dictionary to be loaded
        """
        dic = {}
        cursor = self.con.cursor()
        if dtype == 'dwords':
            cursor.execute('SELECT * FROM dwords')
            for tup in cursor:
                id, word, f = tup
                dic[word] = (id, f)
        elif dtype == 'dctxs':
            cursor.execute('SELECT * FROM dctxs')
            for tup in cursor:
                id, ctx, f = tup
                dic[ctx] = (id, f)
        elif dtype == 'drels':
            cursor.execute('SELECT * FROM drels')
            for tup in cursor:
                idw, idc, f = tup
                dic[(idw, idc)] = f
        else:
            logger.error('Cannot load dictionary of type %d' % dtype)
            return False
        return dic


    def close(self):
        """
        Close an open connection to the database.
        """
        if self.con:
            self.con.close()
#End of SQLite class

class Shelve():
    """
    Class that interact with Shelve files.
    """
    def __init__(self, shname):
        """
        Initiate the class Shelve.

        Parameters:
        -----------
        shname : string
            Location of the shelve file

        Notes:
        ------
        self.sh : shelve instance
            Contains the instance of a shelve when opened
        """
        self.shname = shname
        self.sh = None


    def __get__(self, dicname):
        if self.sh:
            return self.sh[dicname]
        return None

    
    def clear(self):
        """
        Clear dictionaries stored into the shelve.
        """
        self.sh = shelve.open(self.shname, 'n', writeback=True)
        self.sh.close()
    

    def save(self, dic, dtype='dwords'):
        """
        Save the content of a dictionary `dic`

        Parameters:
        -----------
        dic : {DictWords, DictRels} instance
            The dictionary to be saved
        dtype : string {'dwords', 'dctxs', 'drels'}
            The type of dictionary to be saved
        new : Boolean {True, False}, optional
            Create a new table to the dictionary
        """
        self.sh = shelve.open(self.shname, writeback=True)
        self.sh[dtype] = dic.simplify()


    def load(self, dtype='dwords'):
        """
        Load the content of a dictionary `dic`

        Parameters:
        -----------
        dic : {DictWords, DictRels} instance
            The dictionary to be loaded
        dtype : string {'dwords', 'dctxs', 'drels'}
            The type of dictionary to be loaded
        """
        self.sh = shelve.open(self.shname, writeback=True)
        return self.sh[dtype]


    def close(self):
        """
        Close an open connection to the database.
        """
        self.sh.close()
#End of Shelve class


class PlainText(object):
    """
    Class to store elements in Plain text file.
    """
    def __init__(self, fname):
        """
        Parameters:
        -----------
        fname : string
            Path to the text file
        """
        self.fname = fname


    def clear(self):
        """
        Clear dictionaries stored into the shelve.
        """
        for name in ['dwords','dctxs','drels']:
            path = self.fname
            bname = basename(path)
            path = path.replace(bname, name+'_'+bname)
            txt = open(path, 'w', 'utf-8')
            txt.close()


    def save(self, dic, dtype='dwords', transposed=False):
        """
        Save dictionary in a plain text file. 

        Parameters:
        -----------
        dic : {DictWords, DictRels} instance
            The dictionary to be saved
        dtype : string {'dwords', 'dctxs', 'drels'}
            The type of dictionary to be saved
        transposed : boolean {True, False}, optional
            Add the id of the context before the id of the word
        """
        path = self.fname
        bname = basename(path)
        path = path.replace(bname, dtype+'_'+bname)
        with open(path, 'w', 'utf-8') as fout:
            if dtype == 'drels':
                if transposed:
                    fout.write('%%idc idw freq\n')
                else:
                    fout.write('%%idw idc freq\n')
                for key in dic:
                    idw, idc = key
                    f = dic[key]
                    if transposed:
                        fout.write('%d %d %d\n' % (idc, idw, f))
                    else:
                        fout.write('%d %d %d\n' % (idw, idc, f))
            elif dtype == 'dwords' or dtype == 'dctxs':
                if transposed:
                    fout.write('%%id word freq\n')
                else:
                    fout.write('%%word id freq\n')
                for key in dic:
                    id, f = dic[key]
                    if transposed:
                        fout.write('%d %s %d\n' % (id, key, f))
                    else:
                        fout.write('%s %d %d\n' % (key, id, f))
            else:
                logger.error('Cannot save dictionary of type %d' % dtype)
                return False
        return True


    def load(self, dtype='', transposed=False):
        """
        Load dictionary from a plain text file. 

        Parameters:
        -----------
        dtype : string {'dwords', 'dctxs', 'drels'}
            The type of dictionary to be saved
        transposed : boolean {True, False}, optional
            Add the id of the context before the id of the word
        """
        path = self.fname
        bname = basename(path)
        path = path.replace(bname, dtype+'_'+bname)
        dic = {}
        with open(path, 'r', 'utf-8') as fin:
            for line in fin:
                if line.startswith('%%'):
                    continue
                arr = line.strip().split()
                if dtype == 'drels':
                    id1, id2, f = map(int, arr)
                    if transposed:
                        dic[id2, id1] = f
                    else:
                        dic[id1, id2] = f
                elif dtype == 'dwords' or dtype == 'dctxs':
                    if transposed:
                        id, w, f = int(arr[0]), arr[1], int(arr[2])
                    else:
                        w, id, f = arr[0], int(arr[1]), int(arr[2])
                    dic[w] = (id, f)
                else:
                    logger.error('Cannot load dictionary of type %s' % dtype)
                    return False
        return dic


    def close(self):
        """
        Close the file.
        """
        pass
#End of PlainText class
