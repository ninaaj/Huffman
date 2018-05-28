"""
    Christina Trotter
    CSCI 533
    11/29/2017

    This file contains the functions used to compress a given file
"""

import bitstring as bs, huff_heap as h

NUMBITS = 8

def compress(f):
    b,s = encrypt(f), ''
    for l in b:
        s = s + l
    r = len(s) % NUMBITS
    fill_num = NUMBITS - r
    s = s.ljust(len(s) + fill_num,'0')
    bits = bs.BitArray(bin=s)
    byte = bits.tobytes()
    return byte

def encrypt(f):
    f = f.split('\n')
    bits = []
    for line in f:
        chars = list(line)
        bits.append(encrypt_helper(chars))
    bits.append(get_special_bits('EOF'))

    return bits

def get_charbits(c):
    if len(h.heap) < 3:
        return ''
    s = ''
    if c in h.heap[1][1]:
        s = bit_helper(h.heap[1],c,'')
    elif c in h.heap[2][1]:
        s = bit_helper(h.heap[2],c,'')
    s = remove_nones(s)
    return s

def get_special_bits(c):
    a,p,s = 1,0,''

    while a is not h.NO_CHILD:
        p = a
        s = s + str(h.heap[a][3])
        a,b = h.get_children(h.heap,h.heap[a])

    if c == h.heap[p-1][1]:
        s = s[:-1] + str(h.heap[p-1][3])

    return s

def bit_helper(x,c,s):
    s = s + str(x[3])
    if c == x[1]:
        return s
    if c in x[1]:
        a,b = h.get_children(h.heap,x)
        return bit_helper(h.heap[a],c,s), bit_helper(h.heap[b],c,s)
    return

def encrypt_helper(ch):
    bit_str = ''
    for c in ch:
        if c.isalpha() or c == ' ':
            bit_str = bit_str + get_charbits(c.upper())
    bit_str = bit_str + get_special_bits('EOL')
    return bit_str

def remove_nones(x):
    inf = False
    while isinstance(x, tuple) and not inf:
        inf = True
        for y in x:
            if y is not None:
                x = y
                inf = False
    return x
