# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 12:34:15 2021

@author: Logan.Schorr
"""
#import math
import re
import operator as op
import math

#Defining operators to look for in the input
op_pat = re.compile(r'[^\d.]')

#Defining list of operators to choose from
ops = [['^'],['*', '/','%'],['+','-']]

#Defining a global variable to make sure error messages aren't printed more than once
#iterated = False

#Dispatch table to define the actual function used to do the math
ops_table = {'+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            '%': op.mod,
            '^': op.pow
            }

#Iterating through the provided lists to perform the indicated operations
def operator(calc_op,calc_f):
    #While there are any operations in the list, iterate through OOO until all are exhausted
    while calc_op:
        for list in ops:
            for x in list:
                while x in calc_op:
                    #Dummy variable for x so that the while loop does not end until all instances are gone
                    x_mod = x  
                    if (x in ops[1]):
                        #Finding first match of multiplication, division, or modulo and changing dummy variable to the appropriate operation
                        i = next(idx for idx, char in enumerate(calc_op) if char in '*/%')
                        x_mod = calc_op[i]
                    elif (x in ops[2]):
                        #Finding first match of addition or subtraction and changing dummy variable to the appropriate operation
                        i = next(idx for idx, char in enumerate(calc_op) if char in '+-')
                        x_mod = calc_op[i]
                    i = calc_op.index(x_mod)

                    #Performing the operation using the dispatch table
                    calc_f[i] = ops_table[x](calc_f[i],calc_f[i + 1])

                    #Removing the used operation and number from the lists
                    calc_f.pop(i + 1)
                    calc_op.pop(i) 
      
    return calc_f[0]

#Organizing input into operators and numbers
def cal(calc,iterated = False):
    #Creating a list composed of only the operators
    calc_op = op_pat.findall(calc)

    #Splitting the input into a list of only the non operator values
    calc_s = op_pat.split(calc)

    #Searching for blank space caused by double operators and removing it as well as the erroneous operator
    while ("" in calc_s):
        i = calc_s.index("")
        
        #Checking to see if the number is negative and handling it
        if (calc_op[i] in ops[2] and calc_s[i + 1] != ""):
            calc_s[i + 1] = str(ops_table[calc_op[i]](0,float(calc_s[i + 1])))
            calc_op.pop(i)
            calc_s.pop(i)
            continue
        
        #Printing error message that an extra operator was found
        if iterated == False:
            print("An extra operator was found and removed")
            iterated = True

        calc_op.pop(i)
        calc_s.pop(i)

    #Converting all string numerical inputs into floats that can be operated on
    calc_f = [float(x) for x in calc_s]
    
    #Calculating the solution from the parsed inputs
    sol = operator(calc_op,calc_f)
    return sol, iterated

#Working with values inside parentheses
def parenth(inp):
    iterated = False
    #If there aren't an equal number of open and closed, raise an error
    if not (len(re.findall("[(]",inp)) == len(re.findall("[)]",inp))):
        print("Incorrect number of parentheses, unable to interpret")
        quit()

    #Repeat as long as there are parentheses in the input
    while (re.search("[)]",inp)):
        #Finding the first closed set
        c = inp.index(")")
        o = inp.rfind("(",0,c)

        #Splitting the input to isolate closed set and remove the parentheses
        inp_l = [inp[0:o],inp[o+1:c],inp[c+1:]]

        #Checking for implicit multiplication and adding the operators if necessary
        if (inp_l[0] and not op_pat.search(inp_l[0][-1])):
            inp_l[0] = ''.join([inp_l[0],'*'])

        if (inp_l[2] and not op_pat.search(inp_l[2][0])):
            inp_l[2] = ''.join(['*',inp_l[2]])
            
        #Calculating everything inside of the parentheses and converting it into a string
        inp_l[1],iterated = cal(inp_l[1],iterated)
        inp_l[1] = str(inp_l[1])

        #Stitching the string back and removing potential whitespace if a paranthesis was at the beginning or end of the input
        inp = ''.join(inp_l).strip()
    while True:
        #Look for remaining operators to tell if the math is done
        if op_pat.search(inp):
            sol,iterated = cal(inp,iterated)
            break
        sol = inp
        break
    return sol

#Gathering and filtering the user input
def filter():
    while True:
        #Send an input to the user with a prompt asking for an expression
        inp = input("What is the expression that you would like to compute?\n").strip()
        if (len(inp)):
            #Defining the characters that are not accepted to the filter because they are non numerical 
            fil = r'[a-zA-Z!@#$&,`~=;<">\'|[\]{}:?!_]'

            #Searching for the forbidden characters and printing an error if found
            if not (re.search(fil,inp)):
                break
            print("Only numbers and mathematical operators are allowed")
            continue
        print("You must enter an expression")
    return inp

#Rounding function, default is 3 decimal places
def rou(inp,dec = 3):
    if abs(int(inp) - inp) < .001:
        inp = int(inp)
        return inp 
    inp = round(inp,dec)
    return inp

def main():
    calc = filter()
    calc = parenth(calc)
    print(rou(calc))
    return None

main()