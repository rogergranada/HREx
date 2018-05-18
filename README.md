# HREx: A Hierarchical Relation Extraction Tool

This repository contains Python scripts to extract hierarchical relations from plain text files. Hierarchical relations (a.k.a., taxonomic relations) are relations based on the determination of *hypernym* and *hyponym* relations among concepts. As denoted by Jurafsky and Martin [[1](#references)], a concept *c~1~* is considered hypernym of concept *c~2~* if *c~1~* is a generalization of *c~2~*, e.g., the concept *person* is the hypernym of *adult*. Analogously, if *c~1~* is the hypernym of *c~2~*, *c~2~* is the hyponym of *c~1~*, e.g., *adult* is the hyponym of *person*. Once all hypernym/hyponym relations are known the concept hierarchy is constructed. 


## References

[1] Jurafsky, Daniel and Martin, James H. Speech And language processing: An introduction to natural language processing, computational linguistics, and speech recognition. Prentice Hall, 2009.

