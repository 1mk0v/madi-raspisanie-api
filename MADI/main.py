############################################################################################################
#                                                                                                          #
#                                                                                                          #
#                                           ED.                                                            #
#                                           E#Wi                                          .  :             #
#                                           E###G.        t                              ;W  Ef            #
#                ..       :             ..  E#fD#W;       Ej                 ..         f#E  E#t           #
#               ,W,     .Et            ;W,  E#t t##L      E#,               ;W,       .E#f   E#t           #
#              t##,    ,W#t           j##,  E#t  .E#K,    E#t              j##,      iWW;    E#t           #
#             L###,   j###t          G###,  E#t    j##f   E#t             G###,     L##Lffi  E#t fi        #
#           .E#j##,  G#fE#t        :E####,  E#t    :E#K:  E#t           :E####,    tLLG##L   E#t L#j       #
#          ;WW; ##,:K#i E#t       ;W#DG##,  E#t   t##L    E#t          ;W#DG##,      ,W#i    E#t L#L       #
#         j#E.  ##f#W,  E#t      j###DW##,  E#t .D#W;     E#t         j###DW##,     j#E.     E#tf#E:       #
#       .D#L    ###K:   E#t     G##i,,G##,  E#tiW#G.      E#t        G##i,,G##,   .D#j       E###f         #
#      :K#t     ##D.    E#t   :K#K:   L##,  E#K##i        E#t      :K#K:   L##,  ,WK,        E#K,          #
#      ...      #G      ..   ;##D.    L##,  E##D.         E#t     ;##D.    L##,  EG.         EL            #
#               j            ,,,      .,,   E#t           ,;.     ,,,      .,,   ,           :             #
#                                           L:                                                             #
#                                                                                                          #
#                                                                                                          #
#                                        Developed by Potapchuk D.A.                                       #
#                                                                                                          #
############################################################################################################

from .models import *
from bs4 import BeautifulSoup as bs

def remove_spaces(string: str) -> str():

    """Return your input string without double spaces"""

    data = string
    while '  ' in data:
        data = data.replace('  ', ' ')
    if len(data) > 0 and data[len(data)-1] == ' ':
        data = data[:-1]
    return data

def remove_garbage(string: str, symbols: list = []) -> str():

    """Remove garbage from your string"""
    
    name = string
    garbage = ['\n'] + symbols
    for simbol in garbage:
        if simbol in name:
            name = name.replace(simbol, '')
    name = remove_spaces(name)
    return name

def delete_empty_elements(array: List[str]) -> List[str]:
    if array[0] == '' and array[len(array)-1] == '':
        array.pop(0)
        array.pop(len(array) - 1)
    return array