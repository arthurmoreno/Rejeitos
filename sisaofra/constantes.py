from sisaofra.modelo.Fonte import Fonte

def fontes_iniciais():
    #Configuracao das fontes e suas Taxas de Doses
    fontes = []
    taxaDoses = [16.0,18.0,10.0,15.0,
                 17.0,5.0,7.0,8.0,
                 16.5,0.5,1.0,18.0,
                 1.0,17.5,19.0,6.0]
    
    #verificar se os raios se encaixam é outro problema de otimizacao
    raios = [0.6,0.1,0.5,0.3,
             0.2,0.4,0.2,0.2,
             0.3,0.2,0.3,0.2,
             0.1,0.6,0.2,0.6]
    
    for x in range(1,5):
        for y in range(1,5):
            fontes.append(Fonte(str(x)+str(y), taxaDoses[0], raios[0], x, y))
            taxaDoses.remove(taxaDoses[0])
            raios.remove(raios[0])
    return fontes

def calcula_coordenadas_nivel():
    coordenadas = []
    
    #adiciona coordenadas do centro (nivel 1)
    coordenadas.append([])
    i = 0
    for x in range(2,4):
        for y in range(2,4):
            coordenadas[i].append([x, y])
    #adiciona coordenadas do nivel 2
    coordenadas.append([])
    i += 1
    for x in range(1,5):
        for y in range(1,5):
            if not ((x is 2 or x is 3) and 
                    (y is 2 or y is 3)):
                coordenadas[i].append([x, y])
    """
    #adiciona coordenadas do nivel 3
    coordenadas.append([])
    i += 1
    for x in range(1,7):
        for y in range(1,7):
            if not ((x is 2 or x is 3 or x is 4 or x is 5) and 
                    (y is 2 or y is 3 or y is 4 or y is 5)):
                coordenadas[i].append([x, y])
    """
    return coordenadas

def calcula_coordenadas():
    coordenadas = []
    for x in range(1,5):
        for y in range(1,5):
            coordenadas.append([x, y])
    return coordenadas

def calcula_media_relacao_td():
    fontes = fontes_iniciais()
    return sum(list(map(lambda x: x.relacao_td, fontes))) / len(fontes)
        

def receptores():
    lista_receptores = []
    for x in [0,2,3,5]:
        for y in [0,2,3,5]:
            if not ((x is 2 or x is 3) and 
                    (y is 2 or y is 3)):
                lista_receptores.append((x, y))
    return lista_receptores

media_relacao_td = calcula_media_relacao_td()
coordenadas_nivel = calcula_coordenadas_nivel()
coordenadas = calcula_coordenadas()