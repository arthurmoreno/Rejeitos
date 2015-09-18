# from sisaofra.selecao.media import media
# from sisaofra.selecao.roleta import roleta
# from sisaofra.mutacao.janela import janela
"""
:mod:`main` -- Modulo principal
=====================================================================

Modulo para execultar testes dos algoritmos
"""

import time

from sisaofra.constantes import fontes_iniciais
from sisaofra.hibrido_SA_AG.Hibrido import Hibrido
from sisaofra.modelo.Cromossomo import Cromossomo
from sisaofra.modelo.Fonte import Fonte
from sisaofra.mutacao.centraliza import centraliza
from sisaofra.mutacao.colocaFontes import colocaFontes
from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.mutacao.janela import janela
from sisaofra.mutacao.randomPosition import randomPosition
from sisaofra.mutacao.trocaTemperatura import troca_temperatura
from sisaofra.regranegocio.Evolucao import Evolucao
from sisaofra.selecao.extremo import extremo
from sisaofra.utils.Util import calcula_Media, desenha_cromossomo, \
    resultado_excel, log_resultado


if __name__ == '__main__':
    tipo = "Excel"
    #medindo o tempo
    ini = time.time()
            
    cromossomo = Cromossomo('0', fontes_iniciais())
    
    #cromossomo = gera_cromossomo_banco()
    cromossomo.funcao_avaliacao()
    
    """<doc>"""
    print('Cromossomo original')
    print(cromossomo)
    desenha_cromossomo('cromossomo_inicial',cromossomo)
    """</doc>"""
    
    if tipo == "Hibrido":
        #Hibrido - SA
        hibrido = Hibrido()
        
        hibrido.set_Hibrido('teste unico', cromossomo, tam_populacao=100, prob_inicial=0.8, prob_final=0.1, evolucoesH=40, evolucoesAG=50)
        hibrido.set_selecao(extremo, 10)
        hibrido.set_mutacao(troca_temperatura)
        hibrido.set_mutacao_SA(troca_temperatura)
        
        hibrido.evoluir()
    
    elif tipo == "AG":
        #AG - Normal
        evolucao = Evolucao()
        # evolucao.set_evolucao(cromossomo, tam_populacao=100, condicao_parada=50)
        evolucao.set_evolucao(cromossomo, tam_populacao=50, condicao_parada=50)
        
        evolucao.set_selecao(extremo, 2)
        # evolucao.set_selecao(media)
        # evolucao.set_selecao(roleta)
        
        evolucao.set_mutacao(embaralhar)
        # evolucao.set_mutacao(janela, 4, True)
        
        print(evolucao.evoluir())
    elif tipo == 'Excel':
        log_resultado(1, "1", 1, "cromossomo_inicial", cromossomo)
        calcula_Media(5,30)
        resultado_excel(5, 30)
    
    fim = time.time()
    print("Tempo gasto - " + str(fim-ini))
    # TODO: metodo evoluir() retornar: populacao ou melhor cromossomo