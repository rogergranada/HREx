# HREx: A Hierarchical Relation Extraction Tool

This repository contains Python scripts to extract hierarchical relations from plain text files. Hierarchical relations (*a.k.a.*, taxonomic relations) are relations based on the determination of *hypernym* and *hyponym* relations among concepts. As denoted by Jurafsky and Martin [[1](#references)], a concept *c<sub>1</sub>* is considered hypernym of concept *c<sub>2</sub>* if *c<sub>1</sub>* is a generalization of *c<sub>2</sub>*, *e.g.*, the concept *vehicle* is the hypernym of *car*. Analogously, if *c<sub>1</sub>* is the hypernym of *c<sub>2</sub>*, *c<sub>2</sub>* is the hyponym of *c<sub>1</sub>*, *e.g.*, *car* is the hyponym of *vehicle*. Once all hypernym/hyponym relations are known the concept hierarchy is constructed. 

Following WordNet [[2,3](#refereces)], a word *w*<sub>1</sub> is said to be a hypernym of a word *w*<sub>2</sub> if native speakers of English accept the sentence *w*<sub>2</sub> is a (kind of) *w*<sub>1</sub>. Following this definition, a word *w*<sub>2</sub> is a hyponym of a word *w*<sub>1</sub> if *w*<sub>2</sub> is an instance or subclass of *w*<sub>1</sub>, such as *car* is a hyponym of (is a kind of) *vehicle* and *vehicle* is a hypernym (or a semantic class) of *car*. Thus, *Shakespeare* is a hyponym of *author*, (and conversely *author* is a hypernym of *Shakespeare*), *dog* is a hyponym of *canine*, *table* is a hyponym of *furniture*, and so on. The hyponymy relation is transitive and asymmetric, *i.e.*, whenever a word *w*<sub>1</sub> is a hyponym of a word *w*<sub>2</sub>, and *w*<sub>2</sub> is in turn a hyponym of another word *w*<sub>3</sub>, then *w*<sub>1</sub> is also a hyponym of *w*<sub>3</sub>. Asymmetrically, *w*<sub>3</sub> **is not** a kind of *w*<sub>1</sub>. For example, *cab* is a kind of *car* and *car* is a kind of *vehicle*. Thus, by transitivity *cab* is a kind of *vehicle* and by asymmetry *vehicle* **is not** a kind of *cab*. It is important to note that this tool considers taxonomic relations between two concepts as a class inclusion *e.g.*, *chocolate is-a food*, as well as relations between concepts and instances as a class membership relation *e.g.*, *Toblerone is-a chocolate*. 


## References

[1] Jurafsky, Daniel and Martin, James H. Speech And language processing: An introduction to natural language processing, computational linguistics, and speech recognition. Prentice Hall, 2009.  
[2] Miller, George A. and Beckwith, Richard and Fellbaum, Christiane and Gross, Derek and Miller, Katherine J. Introduction to Wordnet: An on-line lexical database. *Journal of Lexicography*, 3(4), pp. 235-244, Oxford Univ Press, 1990.  
[3] Fellbaum, Christiane. WordNet: An electronic lexical database. MIT Press, 1998.  


