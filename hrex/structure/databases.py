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

import sqlite3
import shelve

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


    def _createTable(self, table):
        """
        Create a new table in the database to a dictionary

        Parameters:
        -----------
        table : string {'words', 'contexts', 'relations'}
            Type of table to be created
        """ 
        if table == 'words':
            newTable = """CREATE TABLE dwords(
                            idw INTEGER PRIMARY KEY, 
                            word TEXT, 
                            freq INTEGER
                          );"""
        elif table == 'contexts':
            newTable = """CREATE TABLE dctxs(
                            idc INTEGER PRIMARY KEY, 
                            context TEXT, 
                            freq INTEGER
                          );"""
        elif table == 'relations':
            newTable = """CREATE TABLE drels(
                            idw INTEGER, 
                            idc INTEGER, 
                            freq INTEGER, 
                            FOREIGN KEY (idw) REFERENCES dwords(idw),
                            FOREIGN KEY (idc) REFERENCES dwords(idc),
                            PRIMARY KEY (idc, idw)
                          );"""
        else:
            logger.error('Cannot save dictionary of type %d' % dtype)
            return False
        cur = self.con.cursor()
        cur.execute(newTable)
        self.con.commit()
        return True

    def saveDictionary(self, dic, dtype='words', new=True):
        """
        Save the content of a dictionary `dname`

        Parameters:
        -----------
        dic : dictionary
            The dictionary to be saved
        dtype : string {'words', 'contexts', 'relations'}
            The type of dictionary to be saved
        new : Boolean {True, False}, optional
            Create a new table to the dictionary
        """
        insert = []
        if new:
            self._createTable(dtype)
        if dtype == 'words':
            for word in dic:
                id, freq = dic[word]
                insert.append((word, id, freq))
            cur = self.con.cursor()
            cur.execute('INSERT INTO dwords VALUES (?,?,?)', insert)
            self.con.commit()
        elif dtype == 'contexts':
            for word in dic:
                id, freq = dic[word]
                insert.append((word, id, freq))
            cur = self.con.cursor()
            cur.execute('INSERT INTO dctxs VALUES (?,?,?)', insert)
            self.con.commit()
        elif dtype == 'relations':
            for idw, idc in dic:
                insert.append((idw, idc, dic[(idw, idc)]))
            cur = self.con.cursor()
            cur.execute('INSERT INTO dctxs VALUES (?,?,?)', insert)
            self.con.commit()
        else:
            logger.error('Cannot save dictionary of type %d' % dtype)
            return False
        return True


    def close(self):
        """
        Close an open connection to the database.
        """
        if self.con:
            self.con.close()

class Shelve():
    """
    Class that interact with SQLite3 database.
    """
    def __init__(self, dbname):
        self.db = shelve.open(dbname)

    def __get__(self, dicname):
        return self.db[dicname]
        
