"""
    Christina Trotter
    CSCI 533
    11/29/2017

    This assignment required the use of a leftist heap object instead of a simple binary tree 
    that contains nodes that have pointers to children and parent nodes.  This caused the code
    to become ugly and unnecessarily complicated.

    This file creates a huffman tree (leftist heap) implemented using a list of lists where:
    - every sublist (node) is of length 4:
        * index 0 holds the psuedo index used for mimicking a balanced maxheap
            - every internal node has two children that have the psuedo indexes
              2k+1 and 2k+2 where k is the node's psuedo index
        * index 1 holds the node's key (character/characters from A-Z, space, EOF, EOL)
        * index 2 holds the node's probability (currently useless),
          or in the case of EOL its actual character
        * index 3 holds the node's bit value (left child = 0, right child = 1)
"""
import sys, traceback

BREAK_POINT, EOF, EOL, NO_CHILD, ROOT = 0.5, ['EOF',None,0], ['EOL','\n',1], 'NC', [0,'ROOT',None,None]

def load_data():
    filename = 'huffman.dat'

    data = open(filename, 'r')
    data = data.read()
    data = data.split('\n')

    leaves = []

    for d in data:

        if(len(d) == 0):
            continue

        leaf = d.split(' ')

        a = leaf[0]

        if len(leaf) == 3:
            a,b = ' ',float(leaf[2])
        else:
            b = float(leaf[1])

        leaves.append([a,b])

    s_leaves = sorted(leaves, key=get_value)

    return s_leaves

def heap_it(h,x,l,r):
    a,b = 3,4
    h.append(x)
    h.append([a,l[0][0],l[0][1],l[0][2]])
    h.append([b,r[0][0],r[0][1],r[0][2]])
    r,l = r[1:],l[1:]
    heap_helper(h,a,l)
    heap_helper(h,b,r)
    return

def prep_it(x,l,s):
    b = 1 if s == 0 else 0

    k,v = x[1][0] + x[0][0], x[1][1] + x[0][1]
    
    l.append([x[0][0],x[0][1],b])
    l.append([x[1][0],x[1][1],1])
    l.append([k,v,0])
    for i in range(2,len(x)):

        k,v = x[i][0] + k, x[i][1] + v

        l.append([x[i][0],x[i][1],1])

        if(i == len(x)-1):
            l.append([k,v,s])
        else:
            l.append([k,v,0])
    return

def heap_helper(h,k,n):
    if len(n) == 0:
        return

    a,b = 2 * k + 1, 2 * k + 2
    h.append([b,n[0][0],n[0][1],n[0][2]])
    h.append([a,n[1][0],n[1][1],n[1][2]])
    heap_helper(h,a,n[2:])
    return

def add_special(l):

    x = EOL[0] + EOF[0]
    y = l[0][0] + x

    l.insert(1,[y, None, 0])
    l.insert(0,[x, None, 0])
    l.insert(0,EOL)
    l.insert(0,EOF)

    return

def get_children(h,x):
    a,b = x[0] * 2 + 1, x[0] * 2 + 2
    if any(b in t for t in h):
        i,j = [i for i in h if a in i][0], [j for j in h if b in j][0]
        return h.index(i), h.index(j)
    return NO_CHILD, NO_CHILD #opted for usage of string instead of just returning False

def get_value(x):
    return x[1]

try:
    heap, l_leaves, l_nodes, r_leaves, r_nodes = [],[],[],[],[]
    leaves, l_sum = load_data(), 0
    
    for l in leaves:
        l_leaves.append([l[0],l[1]])
        l_sum = l_sum + l[1]
        if(l_sum >= BREAK_POINT):
            break

    for i in range(len(l_leaves), len(leaves)):
        r_leaves.append([leaves[i][0],leaves[i][1]])

    prep_it(l_leaves,l_nodes,0)
    prep_it(r_leaves,r_nodes,1)
    add_special(l_nodes)

    l_nodes, r_nodes = l_nodes[::-1], r_nodes[::-1]

    heap_it(heap,ROOT,l_nodes,r_nodes)

except Exception as e:
    print(str(e))
    _, _, tb = sys.exc_info()
    print(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])
