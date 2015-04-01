'''
Created on Mar 17, 2015

@author: Suba
'''
import sys

def main():
    file  = open(sys.argv[2])
    outputFile = open("CNF_satisfiability.txt", "w")
    num =  int(file.readline()) + 1
    for i in range (1, num):
        inp = eval(file.readline())
        result = dpllSatisfiable(inp)
        if result != None:
          if result == False:
              outputFile.write(str(["false"]))
              outputFile.write("\n")
          else:
              output = ["true"]
              for key in result:
                  if result.get(key) == True:
                      output.append(key + "=true")
                  else:
                      output.append(key + "=false")
              outputFile.write(str(output))
              outputFile.write("\n")
        else:
          outputFile.write(str(["false"]))
          outputFile.write("\n")

"identify clauses in CNF. The clauses will not have and, or"
def findClauses(cnf):
    try:
        clauses = []
        literal = cnf[0]
        if isinstance(literal, str) and literal == "and":
            for j in range(1, len(cnf)  ):
                l = cnf[j]
                if isinstance( l, str):
                    clauses.append( [l])
                if isinstance( l, list) and l[0]  in ["or"]:
                    newlist = []
                    for k in range (1, len(l)):
                        newlist.append(l[k])
                    clauses.append(newlist)
                if isinstance( l, list) and l[0] in ["not"]:
                    clauses.append( [l])
        if isinstance(literal, str)and literal in [ 'or']:
            for j in range(1, len(cnf)  ):
                l = cnf[j]
                clauses.append( l)
        elif isinstance(literal, str) and literal in ["not"]:
            clauses.append(cnf)
        return clauses
    except: 
        pass


"loops through the clauses, find unit clause"
def findUnitClause(clauses, model):
    try:
            for literal in clauses:
                if len(literal) == 1:
                    return literal[0], True
                if len(literal) == 2 and literal[0] == "not":
                    return literal[1], False
            return None, None
    except: 
        pass


"identify symbols in the given cnf"
def findSymbols(cnf):
    try:
        symbols = []
        for i in iter(cnf):
            if isinstance(i, str) and i not in ["and", "or"] and i not in symbols and ["not", i] not in symbols:
                symbols.append(i)
            elif isinstance(i, list) and i[0] not in ["not"]:
                for j in iter(i):
                    if isinstance(j, str) and j not in ["and", "or"] and j not in symbols and ["not", j] not in symbols:
                        symbols.append(j)
                    elif isinstance(j, list) and j[0] in ["not"] and j not in symbols and j[1] not in symbols:
                        symbols.append(j)
            elif isinstance(i, list) and i[0] in ["not"]:
                    if i[1] not in symbols:
                        symbols.append(i)
        return symbols
    except: 
        pass

"Remove clauses that has symbol, remove [not, symbol] if a clause contains that"
def removeUnitClauses(clauses, symbol):
    try:
        output = []
        for literal in clauses: 
            if symbol in literal:
                pass
            if ["not", symbol] in literal:
                newVal = literal.remove(["not", symbol])
                if newVal == None:
                    output.append([])
                else:
                    output.append(newVal)
        return output
    except: 
        pass

def dpllSatisfiable(cnf):
    try:
        clauses = findClauses(cnf)
        symbols = findSymbols(cnf)
        if isinstance(symbols[0], str) and symbols[0] == "not":
            symbols = [symbols]
        return dpll(clauses, symbols, {})
    except: 
        pass
    
"find pure symbols.(ie) that symbols that occur as only positive or negative"
def findPureSymbols(symbols,clauses, model):
    try:
        pos_occur = False
        negative_occur = False
        for s in symbols:
            currSym = s
            for c in clauses:
                if isinstance(c, str) and c == currSym:
                    pos_occur = True
                if isinstance(c, list) and c[0] == "not":
                    if c == currSym or c[1] == currSym:
                        negative_occur = True
                if isinstance(c, list) and c[0] != "not":
                    for k in c:
                        if isinstance(k, str) and k == currSym:
                            pos_occur = True
                        if isinstance(k, list) and k[0] == "not":
                            if k ==  currSym or k[1] == currSym:
                                negative_occur = True
            if pos_occur and not negative_occur:
                return s, True
            elif negative_occur and not pos_occur:
                return s, False
        return None, None
    except: 
        pass

"remove the clauses that contains symbol"
def removeClauses(clauses, symbol):
    try:
        output = []
        for c in clauses:
            if symbol in c:
                pass
            else:
                output.append(c)
        return output
    except: 
        pass

def dpll(clauses, symbols, model):
    try:
        if clauses == []:
            return model
        clauseCnt = 0
        for c in clauses:
            if c == []:
                return False
            else:
                if isinstance(c, str) and c in model:
                    if not model.get(c):
                        return False
                if isinstance(c, list) and c[0] == "not" and c[1] in model:
                        if model.get(c[1]):
                            return False
                if isinstance(c, list) and c[0] != "not":
                        foundTrue = 0
                        isClauseTrue = False
                        for literal in c:
                            if isinstance(literal, str) and literal in model:
                                foundTrue += 1
                                if  model.get(literal):
                                    isClauseTrue = True
                            if isinstance(literal, list) and literal[0] == "not" and literal[1] in model:
                                foundTrue += 1
                                if not model.get(literal[1]):
                                    isClauseTrue = True
                        if foundTrue == len(c) and isClauseTrue:
                            clauseCnt+= 1
                        if foundTrue == len(c)  and not isClauseTrue:
                            return False
      
        if clauseCnt == len(clauses):
            return model     
    
        P, value = findPureSymbols(symbols, clauses, model)
        if P != None:
            if isinstance(P, list):
                P = P[1]
            model.update({P: value})
            if not value:
                symbols.remove(["not", P])
            else:
                symbols.remove(P)
            "remove all disjuncts that has P"
            clauses = removeClauses(clauses, P)
            return dpll(clauses, symbols, model)
        P, value = findUnitClause(clauses, model)
        if P != None:
            if isinstance(P, list):
                P = P[1]
            model.update({P: value})
            if not value:
                symbols.remove(["not", P])
            else:
                symbols.remove(P)
            "remove all disjuncts that has P"
            clauses = removeUnitClauses(clauses, P)
            return dpll(clauses, symbols, model)
        "split rule"
        P = symbols[0]
        rest = symbols[1:]
        if P != None:
            if isinstance(P, list):
                P = P[1]
        model1 = model.copy()
        model.update({P: True})
        model1.update({P: False})
        return dpll(clauses, rest, model) or dpll( clauses, rest, model1 )
    except: 
        pass
    
if __name__ == "__main__":
    main()