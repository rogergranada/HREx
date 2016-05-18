#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains a class to threat parameters in models. This class should
be inherited by methods in order to set new parameters or load the default.

@author: granada
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger('structure.parameters')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse, os


class Parameters(object):
    """
    Class that set and get parameters to methods.
    """
    def __init__(self, argv):
        """
        Initiate the class Parameters.

        Parameters:
        -----------
        fname : string
            Name of the file that is calling the class
        argv : array_like
            Arguments passed by command line
        """
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('inputfolder', type=lambda x: self._isReadable(parser,x))
        parser.add_argument('outputfile', metavar='file_output', 
            help='the file that the output will be written.', type=lambda x: self._isWritable(parser,x))
        self.args = parser.parse_args()
        self.infile = self.args.inputfolder
        self.outfile = self.args.outputfile

    def inputfile(self):
        """
        Returns:
        --------
        path : string
            The path to the input file.
        """
        return self.infile


    def outputfile(self):
        """
        Returns:
        --------
        path : string
            The path to the output file.
        """
        return self.outfile


    def _isReadable(self, parser, arg):
        """ 
        Makes the test the readability of the argument (folder)
        """
        if os.path.isdir(arg) and os.access(arg, os.R_OK):
            return arg  #return the folder path
        else:
            parser.error('The folder %s is not readable!' % arg)


    def _isWritable(self, parser, arg):
        """ 
        Verifies whether the file exists and whether it is writable. 
        Return the namefile instead of an open file handle.
        """
        if not os.path.isfile(arg) and os.access(arg, os.W_OK):
           parser.error('The file %s does not exist!' % arg)
        else:
           return arg  #return the filename
