from random import shuffle, random
from math import sqrt, fabs
from sisaofra.modelo.Cromossomo import Cromossomo
from sisaofra.modelo.Fonte import Fonte
from sisaofra.constantes import coordenadas, media_relacao_td
from random import uniform
import math

def troca_temperatura(param, T, n_elementos=None):
    """ Mutador atraves do metodo shuffle da classe random do Python
    
    Este metodo embaralha aleatoriamente as posicoes das fontes.
    Se um 'cromossomo' for passado coma parametro, o mesmo sera embaralhado
    Se uma populacao for passado como parametro, todos os cromossomos seram
    embaralhados e a nova populacao sera embaralhada.
    
    :param param: 'Cromossomo' ou list de 'Cromossomos'
    :param n_elementos: Cromossomo (default: None)
    
    FIXME: Ha uma forma mais elegande de fazer isso atraves do __iter__(),
    tornado o metodo iteravel, como ocorre no Cromossomo
    https://docs.python.org/2/library/stdtypes.html
    """
    if isinstance(param, Cromossomo):
        return __embaralhar_cromossomo(param, T)
    elif isinstance(param, list):
        populacao_mutada = []
        i = 0
        for _ in range(n_elementos):
            populacao_mutada.append(__embaralhar_cromossomo(param[i], T))
            i += 1
            if(i >= len(param)):
                i = 0
        return populacao_mutada
    
    """
    if isinstance(param, Cromossomo):
        return __embaralhar_cromossomo(param)
    elif isinstance(param, list):
        populacao_sobra = extremo(param, n_elementos, min)
        populacao_embaralhada = []
        for cromossomo in populacao_sobra:
            populacao_embaralhada.append(__embaralhar_cromossomo(cromossomo))
        return populacao_embaralhada
    """
    
def sort_key(fonte):
    return fonte.relacao_td

def __embaralhar_cromossomo(cromossomo, T):
    
    fontes = cromossomo.fontes
    shuffle(fontes)
    
    i = 0
    while (i+1) < len(fontes):
        centro = [3.5, 3.5]
        i1 = i
        d1 = sqrt((fontes[i1].x - centro[0])*(fontes[i1].x - centro[0]) + (fontes[i1].y - centro[1])*(fontes[i1].y - centro[1]))
        x1 = d1 * fontes[i1].relacao_td
        
        i += 1
        i2 = i
        d2 = sqrt((fontes[i2].x - centro[0])*(fontes[i2].x - centro[0]) + (fontes[i2].y - centro[1])*(fontes[i2].y - centro[1]))
        x2 = d2 * fontes[i2].relacao_td
        
        deltaS = fabs(x1 - x2)
        #print('probabilidade de escolha (mut func): '+str(math.exp(-deltaS / T)))
        #if random() < (1513096 * (-deltaS / T) + (1072693248 - 90.253)):
        if random() < math.exp(-deltaS / T):
            fontes[i1].x, fontes[i2].x = fontes[i2].x, fontes[i1].x
            fontes[i1].y, fontes[i2].y = fontes[i2].y, fontes[i1].y
        i += 1
        
    cromossomo.fontes = fontes
    return cromossomo