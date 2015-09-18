#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: EricK Simoes
'''

class Calculo_dose(object):
    """
    Classe responsavel por realizar o calculo da Camada Semi-Redutora.\n
    Deve ser instanciada com uma String representando o elemento, 
    o valor da respectiva energia do foton, a dose inicial e a espessura do
    material de blindagem.
    """
    
    def __init__(self, elemento='H', energia_foton='0.0', 
                 dose_inicial=0.0, espessura=0.0):
        """
        O construtor assume os sequintes valores padrao para elemento, 
        energia do foton, dose inicial e espessura, respectivamente:
        
        >>> Calculo_dose('H', '0.0', 0.0, 0.0)
        """
        
        self.elemento = '<' + elemento + '>'
        self.energia_foton = energia_foton
        self.dose_inicial = dose_inicial
        self.espessura = espessura
    
    def dose_final(self):
        '''
        Retorna o valor da dose resultante da atenuacao
        '''
        
        print 'Elemento                 -> ' + str(self.elemento)
        print 'Dose inicial             -> ' + str(self.dose_inicial)
        print 'coeficiente de atenuacao -> ' + str(self.coeficiente_atenuacao())
        print 'Espessura:               -> ' + str(self.espessura)
        from math import exp
        dose_final = self.dose_inicial * exp(
            -self.coeficiente_atenuacao() * 
            self.espessura)
        print 'Dose final:              -> ' + str(dose_final)
        return dose_final
    
    def coeficiente_atenuacao(self):
        '''
        Retorna o coeficiente de atenuacao para os 
        valores dos atributos da classe
        '''
        
        with open('../acessodados/coeficiente_atenuacao.txt') as arquivo_txt:
            #Varre o arquivo linha a linha em busca do elemento
            for linha in arquivo_txt:
                #Se o elemento for encontrado, começa a busca pelo coeficiente
                if self.elemento in linha:
                    linha = arquivo_txt.next()
                    while linha.find('<') == -1:
                        from re import findall
                        if findall('\\b%s\\b' %self.energia_foton, 
                        "%s" %linha) != []:
                            return float(linha.split(';')[1])
                        try:
                            #Se chegar no final do arquivo
                            linha = arquivo_txt.next()
                        except StopIteration:
                            break
                    print 'Não encontrado'
    
var = Calculo_dose('He', '3.00000E-03', 10, 4)
var.dose_final()