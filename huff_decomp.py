"""
    Christina Trotter
    CSCI 533
    11/29/2017

    This file contains the functions used to decompress a file compressed using
    the functions in huff_comp.py
"""

import bitstring as bs, huff_heap as h
NUMBITS = 8

def decompress(f):
    bits,b = '', list(f)
    for l in b:
        byte = bin(l)[2:].rjust(NUMBITS, '0')
        bits = bits + byte
    return get_chars(bits)

def get_chars(b):
    if len(h.heap) < 2: 
        return ''

    char_str, c, l = '','',list(b)

    while len(l) > 0:
        if int(l[0]) == h.heap[1][3]:
            l,c = char_helper(h.heap[1],l[1:])
        elif int(l[0]) == h.heap[2][3]:
            l,c = char_helper(h.heap[2],l[1:])
        char_str = char_str + c

    return char_str

def char_helper(x,l):

    if x[1] == 'EOF' or len(l) == 0:
        return [], ''

    a,b = h.get_children(h.heap,x)

    if a == h.NO_CHILD:
        return l, x[1]

    if int(l[0]) == h.heap[b][3]:
        if h.heap[b][1] == 'EOL':
            return l[1:], h.heap[b][2]

        return l[1:], h.heap[b][1]

    if int(l[0]) == h.heap[a][3]:
        return char_helper(h.heap[a],l[1:])

    return
