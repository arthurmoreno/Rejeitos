import random
from sisaofra.modelo.Cromossomo import Cromossomo

def colocaFontes(param, n_elementos=None):
    """ Mutador atraves do metodo shuffle da classe random do Python
    
    Este metodo coloca as fontes em posicoes determinadas para evitar a colisao.
    Se um 'cromossomo' for passado como parametro, o mesmo sera organizado
    Se uma populacao for passado como parametro, todos os cromossomos seram
    organizados e a nova populacao sera embaralhada.
    
    :param param: 'Cromossomo' ou list dos melhores 'Cromossomos'
    :param n_elementos: Cromossomo (default: None)
    
    FIXME: Ha uma forma mais elegande de fazer isso atraves do __iter__(),
    tornado o metodo iteravel, como ocorre no Cromossomo
    https://docs.python.org/2/library/stdtypes.html
    """
    if isinstance(param, Cromossomo):
        return __organizar_cromossomo(param)
    elif isinstance(param, list):
        populacao_mutada = []
        i = 0
        for _ in range(n_elementos):
            populacao_mutada.append(__organizar_cromossomo(param[i]))
            i += 1
            if(i >= len(param)):
                i = 0
        return populacao_mutada
            
    """
        populacao_sobra = extremo(param, n_elementos, min)
        populacao_embaralhada = []
        for cromossomo in populacao_sobra:
            populacao_embaralhada.append(__randomizar_cromossomo(cromossomo))
        return populacao_embaralhada
    """

def __organizar_cromossomo(cromossomo):
    fontes = cromossomo.fontes
    
    random.shuffle(fontes)
    min_x = 1
    min_y = 1
    max_x = 0
    max_y = fontes[0].raio
    i = 0
    maior = 0
    for fonte in fontes:
        if maior < fonte.raio:
            maior = fonte.raio
        if min_x != 1:
            min_x = min_x + fonte.raio
        max_x = min_x + fonte.raio
        if max_x > 7:
            min_x = 1
            max_x = fonte.raio
            min_y = min_y + 2 * maior
            max_y = min_y + maior
            maior = 0
            if max_y > 7:
                max_y = 7
        fonte.x = round(random.uniform(min_x, max_x), 2)
        fonte.y = round(random.uniform(min_y, max_y), 2)
        min_x = fonte.x + fonte.raio
        i += 1
    cromossomo.fontes = fontes
    return cromossomo