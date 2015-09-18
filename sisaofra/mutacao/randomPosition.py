import random
from sisaofra.modelo.Cromossomo import Cromossomo

def randomPosition(param, n_elementos=None):
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
        return __randomizar_cromossomo(param)
    elif isinstance(param, list):
        populacao_mutada = []
        i = 0
        for _ in range(n_elementos):
            populacao_mutada.append(__randomizar_cromossomo(param[i]))
            i += 1
            if(i >= len(param)):
                i = 0
        return populacao_mutada
    
    """
    if isinstance(param, Cromossomo):
        return __randomizar_cromossomo(param)
    elif isinstance(param, list):
        populacao_sobra = extremo(param, n_elementos, min)
        populacao_embaralhada = []
        for cromossomo in populacao_sobra:
            populacao_embaralhada.append(__randomizar_cromossomo(cromossomo))
        return populacao_embaralhada
    """

def __randomizar_cromossomo(cromossomo):
    for fonte in cromossomo:
        fonte.x = round(random.uniform(1, 5), 2)
        fonte.y = round(random.uniform(1, 5), 2)
    return cromossomo