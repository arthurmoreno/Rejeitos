def media(populacao):
    """ Funcao de Selecao por media dos scores.
    
    Seleciona os elementos que estiverem com scores abaixo da media do genoma
    
    Retorna um 'list' com os cromossomos selecionados
    """
    score_total = 0
    novo_populacao = []
    
    for cromossomo in populacao:
        score_total += cromossomo.score[0]
    media = score_total / len(populacao)
    
    for cromossomo in populacao:
        if cromossomo.score[0] <= media:
            novo_populacao.append(cromossomo)
    return novo_populacao
