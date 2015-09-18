"""
:mod:`Fonte` -- modulo que representa a fonte armazenada no deposito de rejeito
=====================================================================

Neste modulo esta implementado todos os
procedimentos relacionados as fontes radioativas.
"""

from math import sqrt

class Fonte(object):
    
    def __init__(self, identificador, taxaDose, raio, x, y):
        """ Classe Fonte - Fonte radioativa do predio de rejeitos
            
        Exemplo:
            >>> fonte = Fonte('A', 2.3, 1, 1)
            >>> fonte.calculaTaxaDose(6)
    
        :param identificador: identificador da fonte
        :param taxaDose: o valor da taxa de dose da fonte
        :param x: a posicao da fonte em x
        :param y: a posicao da fonte em y
        
        :attention: As posicoes x e y da fonte devem ser maiores que zero
        """
        self.identificador = identificador
        self.taxa_dose = taxaDose
        self.raio = raio
        self.x = x
        self.y = y
        if self.raio > 0.0:
            self.relacao_td = self.taxa_dose / (2 * self.raio)
        else:
            self.relacao_td = 0 # para as dummys fontes

    def __repr__(self):
        ret = "- Fonte %s\n" % (self.identificador)
        ret += "\tTaxa de Dose:\t %s\n" % (self.taxa_dose)
        ret += "\tCoordenadas:\t %sx%s\n" % (self.x, self.y)
        return ret
    
    def __eq__(self, outra_fonte):
        """ equals - Sobrescreve o metodo equals dos objetos Python.
    
         Duas fontes sao iguais quando possuem a mesma taxa de dose, x e y.
        
        :param outra_fonte: 'Fonte' a ser comparada
        :rtype: 'bool'
        
        TODO: futuramente, tambem seram iguais se tiverem a mesma blindagem
        """
        return self.taxa_dose == outra_fonte.taxa_dose and self.x == outra_fonte.x and self.y == outra_fonte.y
    
    def calcula_taxa_dose(self, x_receptor, y_receptor):
        """ calculaTaxaDose - Calcula a Taxa de Dose
        mo:        49
        Score:     26.1999748617
        Leva em consideracao a taxa de dose da fonte e a distancia do receptor,
        considerando sempre como 1 o valor inicial da distancia
        
        """
        
        #return self.taxa_dose / (((x_receptor - self.x) ** 2) + ((y_receptor - self.y) ** 2))
        denominador = (((x_receptor - self.x) * (x_receptor - self.x)) + ((y_receptor - self.y) * (y_receptor - self.y)))
        if denominador == 0:
            denominador = 0.00001
        return self.taxa_dose / denominador
