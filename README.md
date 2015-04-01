# 3SAT-solver
Python based 3 SAT solver. 

The CNF converter script takes propositional sentences as input and converts them into CNF form. 
Arguments to run are -i sentences.txt where sentences.txt contains sentences in propositional form. 
The first line of the file contains the number of sentences. 

DPLL.py is the implementation of DPLL algorithm. It takes sentences in CNF form and checks for satisfiability.
If a sentence is satisfiable, the assignments that makes the sentnece are recorded. 
Arguments to run is -i CNFsentences.txt wher CNFsentences.txt has CNF sentences. 
It is assumed that all sentences are in proper format.
