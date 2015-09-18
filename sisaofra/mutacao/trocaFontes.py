# -*- coding: latin-1 -*-

from random import randint
from sisaofra.selecao.extremo import extremo
from sisaofra.modelo.Cromossomo import Cromossomo

def trocaFontes(param, n_elementos=None):
    """Mutador que troca duas fontes de lugar
    
    Este metodo troca o lugar de duas fontes e substitui
    o valor de suas posições uma com a outra. Este metodo
    se aproxima mais com uma função de vizinhança, para ser
    utilizado no simulated annealing.
    
    :param param: 'Cromossomo' ou list de 'Cromossomos'
    :param n_elementos: Cromossomo (default: None)
    
    FIXME: Ha uma forma mais elegande de fazer isso atraves do __iter__(),
    tornado o metodo iteravel, como ocorre no Cromossomo
    https://docs.python.org/2/library/stdtypes.html
    """
    
    if isinstance(param, Cromossomo):
        return __trocar_cromossomo(param)
    elif isinstance(param, list):
        populacao_mutada = []
        i = 0
        for _ in range(n_elementos):
            populacao_mutada.append(__trocar_cromossomo(param[i]))
            i += 1
            if(i >= len(param)):
                i = 0
        return populacao_mutada
    
    """
    if isinstance(param, Cromossomo):
        return __trocar_cromossomo(param)
    elif isinstance(param, list):
        populacao_sobra = extremo(param, n_elementos, min)
        populacao_trocada = []
        for cromossomo in populacao_sobra:
            populacao_trocada.append(__trocar_cromossomo(cromossomo))
        return populacao_trocada
    """

def __trocar_cromossomo(cromossomo):
    fonte1 = cromossomo.fontes.pop(randint(0,15))
    fonte2 = cromossomo.fontes.pop(randint(0,14))
    
    tempTaxaDose = fonte1.taxa_dose
    fonte1.taxa_dose = fonte2.taxa_dose
    fonte2.taxa_dose = tempTaxaDose
    
    cromossomo.fontes.append(fonte1)
    cromossomo.fontes.append(fonte2)
    return cromossomo