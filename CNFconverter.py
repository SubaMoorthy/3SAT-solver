'''
Created on Mar 8, 2015

@author: Suba
'''
import sys

def main():
    try:
        file  = open(sys.argv[2])
        outputFile = open("sentences_CNF.txt", "w+")
        num =  int(file.readline()) + 1
        for i in range (1, num):
            inp = eval(file.readline())
            step1 = replaceIff(inp)
            step2 = replaceImplies(step1)
            step3 = moveNotInside(step2)
            step4 = deMorgansLaw(step3)
            step5 = removeDuplicateSymbols(step4)
            final = removeDuplicateLiterals(step5)
            if final != None:
                outputFile.write(str(final))
            else:
                outputFile.write("")
            outputFile.write("\n")
    except:
        pass
       
"if sentnce has iff, replace it" 
def replaceIff(cnf_curr) :  
    try:
        if isinstance(cnf_curr, list) :
            sym = cnf_curr[0].lower()
            if sym == "not" :
                child = replaceImplies(cnf_curr[1])
                cnf_next = ["not", child]
            else : 
                lhs = replaceImplies(cnf_curr[1])
                rhs = replaceImplies(cnf_curr[2])
                if sym == "iff" :
                    cnf_next = ["and",["implies",  lhs, rhs], ['implies', rhs,lhs]]
                else :  
                    cnf_next = [sym, lhs, rhs]
        else :
            cnf_next = cnf_curr
        return cnf_next
    except: 
        pass
    
"if sentence has implies replace it"
def replaceImplies(cnf_curr) :  
    try:
        if isinstance(cnf_curr, list) :
            sym = cnf_curr[0].lower()
            if sym == "not" :
                child = replaceImplies(cnf_curr[1])
                cnf_next = ["not", child]
            else : 
                lhs = replaceImplies(cnf_curr[1])
                rhs = replaceImplies(cnf_curr[2])
                if sym == "implies" :
                    cnf_next = ["or", ["not", lhs], rhs]
                else :  
                    cnf_next = [sym, lhs, rhs]
        else :
            cnf_next = cnf_curr
        return cnf_next
    except:
        pass
 
"if there is not move it inside the sentence. change the operation accordingly. Remove double negations if any"   
def moveNotInside(cnf_curr) :
    try: 
        if isinstance(cnf_curr, str) :
            cnf_next = cnf_curr
        else :  
            sym = cnf_curr[0].lower()
            if sym == "not":
                arg = cnf_curr[1]
                if isinstance(arg, str) :
                    cnf_next = ["not"  , arg] 
                else :  
                    inner_op = arg[0]
                    if inner_op == "not" :
                        cnf_next = moveNotInside(arg[1])
                    else : 
                        lhs = moveNotInside(["not", arg[1]])
                        rhs = moveNotInside(["not", arg[2]])
                        dual = {"and": "or",  "or": "and"} 
                        cnf_next = [dual[inner_op], lhs, rhs] 
            else : 
                lhs = moveNotInside(cnf_curr[1])
                rhs = moveNotInside(cnf_curr[2])
                cnf_next = [sym, lhs, rhs]
        return cnf_next
    except:
        pass
    
"Apply DeMorgan's law"
def deMorgansLaw(cnf_curr) :
    try: 
        if isinstance(cnf_curr, str) : 
            cnf_next = cnf_curr
        else :  
            sym = cnf_curr[0].lower()
            if sym == "and":
                lhs =  deMorgansLaw(cnf_curr[1])
                rhs =  deMorgansLaw(cnf_curr[2])
                cnf_next = ["and", lhs, rhs]
            if sym == "or": 
                lhs =  deMorgansLaw(cnf_curr[1])
                rhs =  deMorgansLaw(cnf_curr[2])
                cnf_next = applyDistibutiveLaw(lhs, rhs)
            if sym == "not":
                cnf_next = cnf_curr        
        return cnf_next
    except:
        pass

"To handle nested operators - recursion"
def applyDistibutiveLaw(lhs, rhs):  
    try:
        if isinstance(lhs, list) and lhs[0] == "and" :
            answer = ["and", applyDistibutiveLaw(lhs[1],rhs), applyDistibutiveLaw(lhs[2], rhs)]
        elif  isinstance(rhs, list) and rhs[0] == "and" :
            answer = ["and", applyDistibutiveLaw(lhs,rhs[1]), applyDistibutiveLaw(lhs,rhs[2])]
        else :
            answer = ["or", lhs, rhs]
        return answer
    except:
        pass

"To remove duplicate variables"
def removeDuplicateLiterals(cnf):
    try:
        answer = []
        for i in cnf:
            if isinstance(i, str) and i not in answer:
                answer.append(i)
            if isinstance(i, list):
                answer.append(removeDuplicateLiterals(i))
        j = 0
        for i in answer:
            j += 1;
            if i in ['and', 'or'] and len(answer) - j %2 == 1:
                answer.remove(i)
        for i in  range(1,len(answer)-1):
            j = i + 1
            if sorted(answer[i]) == sorted(answer[j]):
                answer.remove(answer[i])
        return answer
    except:
        pass

"Remove duplicate occurences of symbols in nested scenario (Associative Law)"
def removeDuplicateSymbols(cnf_curr):
    try:
        cnf_next = []
        temp = cnf_curr[:]
        sym = ""
        for j in range(0, len(cnf_curr)):
            i = cnf_curr[j]
            if isinstance(i, str) and i in ["and", "or"]:
                sym = i
            if isinstance(i, str):
                cnf_next.append(i)
            if isinstance(i, list) and sym != "" and i[0] == sym:
                temp.remove(i)
                for k in range(1, len(i)):
                    cnf_next.append(i[k])
        for i in temp:
            if isinstance(i, list) and i not in cnf_next:
                if i[0] != "not":
                    x = removeDuplicateSymbols(i)
                else:
                    x = i
                cnf_next.append(x)
        return cnf_next
    except:
        pass
    

if __name__ == "__main__":
    main()
    