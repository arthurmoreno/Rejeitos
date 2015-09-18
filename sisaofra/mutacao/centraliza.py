from random import shuffle
from sisaofra.modelo.Cromossomo import Cromossomo
from sisaofra.modelo.Fonte import Fonte
from sisaofra.constantes import coordenadas_nivel, media_relacao_td
from random import uniform

def centraliza(param, n_elementos=None):
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
        return __centraliza_cromossomo(param)
    elif isinstance(param, list):
        populacao_mutada = []
        i = 0
        for _ in range(n_elementos):
            populacao_mutada.append(__centraliza_cromossomo(param[i]))
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

def __centraliza_cromossomo(cromossomo):
    #media = media_relacao_td
    vetor_posicoes = coordenadas_nivel
    nivel_1 = vetor_posicoes[0]
    nivel_2 = vetor_posicoes[1]
    nivel_3 = vetor_posicoes[2]
    shuffle(nivel_1)
    shuffle(nivel_2)
    shuffle(nivel_3)
    
    cromossomo.fontes = sorted(cromossomo.fontes, key=sort_key, reverse=True)
    
    i1 = 0
    i2 = 0
    i3 = 0
    for fonte in cromossomo:
        if i1 < len(nivel_1):
            fonte.x = nivel_1[i1][0] + uniform(-0.05, 0.05)
            fonte.y = nivel_1[i1][1] + uniform(-0.05, 0.05)
            i1 += 1
        elif i2 < len(nivel_2):
            fonte.x = nivel_2[i2][0] + uniform(-0.05, 0.05)
            fonte.y = nivel_2[i2][1] + uniform(-0.05, 0.05)
            i2 += 1
        elif i3 < len(nivel_3):
            fonte.x = nivel_3[i3][0] + uniform(-0.05, 0.05)
            fonte.y = nivel_3[i3][1] + uniform(-0.05, 0.05)
            i3 += 1
    return cromossomo