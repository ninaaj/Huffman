"""
    Christina Trotter
    CSCI 533
    11/29/2017
    This is the main py file. Run it to compress and decompress files
"""

import huff_comp as hc, huff_decomp as hd, os, sys, traceback

MENU = '\nPick a task:\n[C]ompress a file\n[D]ecompress a file\n[Q]uit\n\nCHOICE: '
INVL = '\nInvalid Input\nPlease enter C/c, D/d, or Q/q\n'
ENTR, NFF = '\nEnter a filename: ', '\nSorry! {} was not found'
COMP, DECO, QUIT = ['C','c'],['D','d'],['Q','q']
CHOICES = [COMP,DECO,QUIT]

def compress(f):
    d = open(f, 'r')
    d = d.read()
    cd = hc.compress(d)
    cf = f + '.huff'
    cmpr = open(cf, 'wb+')
    cmpr.write(cd)
    cmpr.close()
    print('..file compression complete..\nfile saved as ',cf)
    return

def decompress(f):
    if f[-5:] != '.huff':
        print('Sorry! I can only decompress files I previously compressed.')
        return
    d = open(f, 'rb')
    d = d.read()
    dd = hd.decompress(d)
    print(dd)
    print('..file decompression complete..')
    return

try:
    ch = ''
    print('\n~HUFFMAN FILE COMPRESSOR~') 
    while ch not in QUIT:
        ch = input(MENU)
        if not any(ch in c for c in CHOICES):
            print(INVL)
            continue
        if ch in COMP:
            print('\n~COMPRESSION~')
            filename = input(ENTR)
            if os.path.isfile(filename):
                compress(filename)
            else:
                print(NFF.format(filename))
        elif ch in DECO:
            print('\n~DECOMPRESSION~')
            filename = input(ENTR)
            if os.path.isfile(filename):
                decompress(filename)
            else:
                print(NFF.format(filename))

    print('\nGOODBYE!\n')

except Exception as e:
    print(str(e))
    _, _, tb = sys.exc_info()
    print(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])
