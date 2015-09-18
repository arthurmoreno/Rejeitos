from random import shuffle
from sisaofra.modelo.Cromossomo import Cromossomo
from sisaofra.modelo.Fonte import Fonte
from sisaofra.constantes import coordenadas, media_relacao_td
from random import uniform

def embaralhar(param, n_elementos=None):
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
        return __embaralhar_cromossomo(param)
    elif isinstance(param, list):
        populacao_mutada = []
        i = 0
        for _ in range(n_elementos):
            populacao_mutada.append(__embaralhar_cromossomo(param[i]))
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

def __embaralhar_cromossomo(cromossomo):
    #media = media_relacao_td
    vetor_posicoes = coordenadas
    shuffle(vetor_posicoes)
    
    i = 0
    for fonte in cromossomo:
        fonte.x = vetor_posicoes[i][0] + uniform(-0.05, 0.05)
        fonte.y = vetor_posicoes[i][1] + uniform(-0.05, 0.05)
        i += 1
    return cromossomo