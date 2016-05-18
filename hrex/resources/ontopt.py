#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module extract and iterate with Onto.PT elements. Onto.PT (Ontologia Lexical
para o Portugues) is a public lexical ontology for Portuguese. Onto.PT
is the result of the automatic exploitation of Portuguese dictionaries and thesauri,
and it aims to minimise the main limitations of existing Portuguese lexical
knowledge bases \cite{OliveiraAndGomes2014}. Onto.PT is available at 
`Onto.PT <http://ontopt.dei.uc.pt/>`_.

@author: rogergranada
""" 
import sys
sys.path.insert(0, '..')

import logging
logger = logging.getLogger('resources.ontopt')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#logging.basicConfig(format='%(message)s',level=logging.INFO) #filename='patterns.log'
 
# Set standard output encoding to UTF-8.
from codecs import getwriter, open
sys.stdout = getwriter('UTF-8')(sys.stdout)
from os.path import join

from utils import Arguments
from taxonomy.misc import *
import dictionaries
from corpus import shelves
from shelves import MatrixWriter
from structure import graph

class OntoPT:
    def __init__(self, dirin, dcpt=None, load_synsets=False, delgraph=False, delsyn=False):
        """
        Generate methods to deal with a shelve file containing OntoPT.
        input:
            dirin: must contain the OntoPT in shelve format, namely ``ontoPT.db''.
        """
        self.fonto = join(dirin, 'ontoPT.db')
        self.dsyns = dictionaries.DictList()
        self.dsyns.load_shelve(self.fonto, dbname='synsets') #[syn1]: [noun1, noun2, ...]
        self.dnouns = self.dsyns.transpose()            #[noun]: [syn_1, syn_2, ...]
        self.grels = graph.Graph()
        if dcpt:
            self.dcpt = dcpt
        else:
            self.dcpt = dictionaries.DictWords()
        self.dHs = {}
        self.dwords = {}

        if load_synsets:
            self.load_synsets()
        if delgraph:
            del self.grels
        if delsyn:
            del self.dsyns
            del self.dnouns


    def load_synsets(self):
        """
        Load self.dcpt to perform searching of Hypernyms-hyponyms.
        input:
            dcpt: contains the dictionary of words in the format:
                [word]: (id, tf)
        output:
            self.dHs: set of synsets hypernyms. It has the form:
                [idw]: set(idsyn_parent_1, idsyn_parent_2, ...)
            self.dwords: set of IDs of synsets in which ``word'' occurs.
                It has the form:
                [idw]: set(idsyn_1, idsyn2, ...)
        """ 
        logger.info('accepted dictionary containing %d words' % len(self.dcpt))
        logger.info('verifying relations in OntoPT')
        self.grels.load_shelve(self.fonto, dbname='graph')
        pb = ProgressBar(len(self.dcpt))
        for word in self.dcpt:
            if self.has_word(word):
                #id = self.dcpt_id(word)
                id, _ = self.dcpt[word]
                self.dwords[id] = set(self.dnouns[word])            # set
                #self.dHs[id] = self.parent_synset_hypernyms(word)   # set
                self.dHs[id] = self.all_synsets_hypernyms(word)     # set
            pb.update()
        logger.info('found %d words in OntoPT' % len(self.dwords))
        logger.info('reducing dictionary: %d to %d' % (len(self.dcpt), len(self.dHs)))
        return True
                    

    #def dcpt_id(self, word):
    #    """
    #    Return the ``id'' of a certain word in the dictionary
    #    of concepts (dcpt). Attention: this id correspond to
    #    the ids in corpus and not in OntoPT.
    #    """
    #    if isinstance(self.dcpt[word], tuple):
    #        id, _ = self.dcpt[word]
    #    else:
    #        id = self.dcpt[word]
    #    return id


    def is_hypernym(self, v1, v2, mode='id'):
        """
        Verify if ``v1'' is hypernym of ``v2''. It returns:
           1: In case v1 > v2 (v1 is hypernym of v2)
           0: In case v1 ! v2 (v1 is not hypernym of v2)
          -1: In case v1 < v2 (v2 is hypernym of v1)
        ``mode'' correspond to the value of ``v1'' and ``v2''.
            mode='id': v1 correspond to the id of a synset
            mode='word': v1 correspond to the noun in a synset.
        """
        if mode == 'id':
            idw1 = v1
            idw2 = v2
        elif mode == 'word' and self.dcpt:
            idw1 = self.dcpt[v1]
            idw2 = self.dcpt[v2]
        else:
            logger.error('dictionary "dcpt" not loaded!')
            sys.exit(1)
        sw1 = self.dHs[idw1]
        sw2 = self.dHs[idw2]
        if sw2.intersection(self.dwords[idw1]):
            return 1
        elif sw1.intersection(self.dwords[idw2]):
            return -1
        else:
            return 0


    def synsets(self, word):
        """
        Return the synsets IDs that contains ``word''.
        """
        return self.dnouns[word]


    def all_lemmas(self, word):
        """
        Return all lemmas associated to a synset containing ``word''.
        """
        lemmas = []
        for synset in self.dnouns[word]:
            lemmas.extend(self.dsyns[synset])
        return set(lemmas)


    def lemmas_from_synset(self, synset):
        """
        Return all lemmas associated to a certain synset.
        """
        return self.dsyns[synset]

    
    def set_of_hypernyms(self, key, mode='id'):
        """
        Return a set contaning all hypernyms of ``key''.
        """
        if mode == 'id':
            idw = key
        elif mode == 'word':
            idw, _ = self.dcpt[key]
        return self.dHs[idw]


    def all_synsets_hypernyms(self, word):
        """
        Return all hypernyms of a certain word. It uses the
        structure of the graph to find out all ascendents.
        """
        synH = []
        for synset in self.dnouns[word]:
            synH.extend(self.grels.get_ancestors(synset))
        return set(synH)


    def parent_synset_hypernyms(self, word):
        """
        Return the direct hypernyms of a certain word. It uses the
        structure of the graph to find out the predecessors.
        """
        synH = []
        for synset in self.dnouns[word]:
            synH.extend(self.grels.get_parents(synset))
        return set(synH)


    def parents_of_synset(self, idsyn):
        """
        Return the direct hypernyms of a certain synset. It uses the
        structure of the graph to find out the predecessors.
        """
        return self.grels.get_parents(idsyn)


    def nlevel_synset_hypernyms(self, word, levels=1):
        """
        Return the all hypernyms up to ``level'' of a certain word. 
        It uses the structure of the graph to find out the predecessors.
        """
        stmp = set(self.dnouns[word])
        synH = []
        if levels == 0:
            return stmp
        for level in range(levels):
            ltmp = []
            for synset in stmp:
                parents = self.grels.get_parents(synset)
                ltmp.extend(parents)
                synH.extend(ltmp)
            stmp = set(ltmp)
        return set(synH)


    def has_word(self, word):
        """
        Verify whether ``word'' exists in OntoPT.
        """
        if self.dnouns.has_key(word):
            return True
        else:
            return False


    def filter_dictionary(self, dcpt=None, transpose=False):
        """
        Filter out words that not appear in OntoPT graph.
        Return a new dictionary containing only terms that
        appear in OntoPT.
            input: 
            self.dcpt: dictionaries.DictWords() [w]: (id, tf)
            output:
            dfiltered: dictionaries.DictWords() [w]: (id, tf)
        """
        if not dcpt:
            if self.dcpt:
                dcpt = self.dcpt
            else:
                logger.error('there is no dictionary of words "dcpt"')
                sys.exit(1)
        
        logger.info('verifying terms in OntoPT')
        dfiltered = dictionaries.DictWords()
        for word in dcpt:
            if self.has_word(word):
                id, tf = dcpt[word]
                #id = self.dcpt_id(word)
                if transpose:
                    dfiltered[id] = (word, tf)
                else:
                    dfiltered[word] = (id, tf)
        logger.info('found %d words in OntoPT' % len(dfiltered))
        logger.info('reducing dictionary: %d to %d' % (len(dcpt), len(dfiltered)))
        return dfiltered
#End of class OntoPT

def generate_relations_graph(dirout):
    """
    Generate a graph ``Graph()'' containing all relations
    from ``drels'' in ``ontopt.db''. This graph is saved
    into ``ontopt.db'' with the name ``graph''.
    """
    fonto = join(dirout, 'ontoPT.db')
    drels = dictionaries.DictList()
    drels.load_shelve(fonto, dbname='relations')
    G = graph.Graph(drels, notransit=False)
    del drels
    G.save_as_shelve(fonto, dbname='graph', append=True)
    return G

def parse_rdf(rdffile, dirout):
    """
    Receive a .rdf file containing Onto.PT structure and extract
    all relations between hypernym-hyponym synsets. It generates 
    as output two dictionaries:
    ``dsyns'': contains the id of each synset and the content of
    the synset (list of nouns).
        [idsyn] = [noun_1, noun_2, ...]
    ``dHh'': contains the id of the hyponym synset and its list 
    of hypernym synsets.
        [idh] = [idH_1, idH_2, ...]
    """
    import rdflib
    logger.info('parsing triples from RDF file: %s' % rdffile)
    URI = 'http://ontopt.dei.uc.pt/OntoPT.owl#'
    g = rdflib.Graph()
    result = g.parse(rdffile)

    dNomeSyn = {}         #contain the id of the synset when it's a noun synset
    dallsyns = dictionaries.DictList() #[idsynset]: [noun1, noun2, ...]
    dHh = {}         #[(idH, idh)]: ''

    for subj, pred, obj in g:
        idsubj = subj.replace(URI, '')
        idpred = pred.replace(URI, '')
        idobj = obj.replace(URI, '')
        
        if idsubj.isdigit():
            idsubj = int(idsubj)
            if idobj == 'NomeSynset':
                dNomeSyn[idsubj] = ''
        
            if idpred == 'formaLexical':
                dallsyns[idsubj] = idobj
                
            if idpred == 'hiperonimoDe':
                dHh[(int(idsubj), int(idobj))] = ''
            
            if idpred == 'hiponimoDe':
                dHh[(int(idobj), int(idsubj))] = ''

    logger.info('building relations only for NomeSynset elements')
    #keep only NomeSynset in relations and remove H>h == h>H
    drels = dictionaries.DictList() #[idh]: [idH1, idH2, ...]
    dsyns = dictionaries.DictList() #[idsynset]: [noun1, noun2, ...]
    for idH, idh in dHh: 
        #idH and idh are NomeSynsets, have formaLexical and there's no cycle
        if dNomeSyn.has_key(idH) and dNomeSyn.has_key(idh)     \
           and dallsyns.has_key(idH) and dallsyns.has_key(idh) \
           and not dHh.has_key((idh, idH)):                         
            drels[idh] = idH
            if not dsyns.has_key(idH):
                dsyns[idH] = dallsyns[idH]
            if not dsyns.has_key(idh):
                dsyns[idh] = dallsyns[idh]
    del dHh
    return dsyns, drels

def gen_OPT(dirin):
    fout = open(join(dirin, 'ontopt.rls'), 'w')
    db = shelves.MatrixReader(join(dirin, 'w5_onto.db'))
    dcpt = db.dic_words(transposed=False)
    onto = OntoPT(dirin, dcpt=dcpt, load_synsets=True, delgraph=True, delsyn=True)
    dcpt_t = dcpt.transpose()

    keys = dcpt_t.keys()
    for index1 in range(len(keys)):
        icpt1 = keys[index1]
        for index2 in range(index1+1, len(keys)):
            icpt2 = keys[index2]
            order = onto.is_hypernym(icpt1, icpt2, mode='id')
            if order == 1:
                fout.write('%d %d\n' % (icpt1, icpt2))
            if order == -1:
                fout.write('%d %d\n' % (icpt2, icpt1))
    fout.close()
    logger.info('relations saved into %s/wordnet.rls' % dirin)

def main(argv):
    t = TimeRecorder()
    desc ="Create ontoPT.db shelve."
    required = [desc, 'inputfile', 'outputfolder']
    args = Arguments(required).getArgs()
    filein, dirout = args.inputfile, args.outputfolder
    
    #Generate dictionaries from Onto.PT RDF file
    #dsyns, drels = parse_rdf(filein, dirout)
    #dsyns.save_as_shelve(join(dirout, 'ontoPT.db'), dbname='synsets', append=False)
    #drels.save_as_shelve(join(dirout, 'ontoPT.db'), dbname='relations', append=True)

    #Generate a graph of the whole net of relations
    generate_relations_graph(dirout)

    #Load dictionaries
    #dcpt = {'ano': 1, 'dog': 2, 'sentido': 3, 'meio': 4}
    #ontopt = OntoPT(dirout, dcpt)
    #print ''
    #print ontopt.nlevel_synset_hypernyms('ano', levels=2)
    #print ontopt.parent_synset_hypernyms('ano')
    #print ontopt.parents_of_synset(25673)
    #print ontopt.is_hypernym(4, 1)
    #print ontopt.is_hypernym(1, 3)

    t.end()

if __name__ == "__main__":
    main(sys.argv)
