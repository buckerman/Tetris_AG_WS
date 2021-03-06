########################################################################################
##                                  ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2017     ##
##      https://www.facebook.com/grupoturing.poliusp        ##
##      Todos podem usar este codigo livremente         ##
##                                  ##
########################################################################################

import pygame
import random

import tetris as t

#########################################################################################

### A classe Individuo incializa o individuo com score nulo e um vetor de pesos.
### Ela tambem implementa a funcao fitness utilizada para avaliar o score de cada individuo
### e calcula a direcao para a qual o jogador se move (para esquerda ou direita e se deve rotacionar) a partir
### do resultado calculado multiplicando-se o vetor de pesos daquele individuo por uma
### entrada.

## Reflexao: O que o vetor entrada contem?

class Individuo():

    # Inicializa o individuo com vetor pesos e score nulo.
    def __init__(self,pesos):
        self.pesos = pesos
        self.score = 0

   # Forma de visualizar ao utilizar a funcão print
    def __str__(self):
        # nao precisa mexer aqui
        # retorna o print do individuo facil de ler
        s = "   Pesos:"
        for i in range(len(self.pesos)):
            s+= "%5.2f "%(self.pesos[i])
        return s

    ### ------------------- fitness:
    ## A funcao fitness foi calculada a partir 
    ## Vale a reflexao: qual outra forma de se pensar na funcao fitness?
    ## COMPLETE AQUI:
    def fitness(self,gameState):
        #gameState = [numero de pecas, linhas destruidas(combos de 1,2,3,4), score normal de tetris, ganhou]
        #k1*t - abs(deltaY(morreu)[player-bolinha))
        self.score = gameState[0]


    ### ------------------- calcular_saida:
    ## Seleciona a direcao em que o jogador vai se mover a partir do valor computado pelo
    ## produto entre o vetor entrada e o vetor pesos de cada individuo. Se esse valor
    ## for maior que meio, o jogador sobe, caso contrario ele desce.

    ## Vale a reflexao: qual outra forma de implementar a decisao a partir do valor obtido
    ## na variavel `saida`? Nesse caso utilizou-se uma decisao binaria.
    def calcularMelhorJogada(self, board, peca, jogoRapido = False):
        
        melhorX = 0 #posicao em x
        melhorR = 0 #rotacao da peca
        melhorY = 0
        melhorScore = -100000 #menor do q qualquer valor de score

        #calcula buracos e tampas inicias
        buracosTotaisAntes, tampasTotaisAntes = t.calcularInfosIniciais(board)
            
        for r in range(len(t.PIECES[peca['shape']])):  #itera em todas as rotaçoes possiveis
            for x in range(-2,t.BOARDWIDTH-2):         #iterar todas as posicoes possiveis

                #retorna: [jogadaValida, alturaTotal, numLinhasCompletas, buracosFormados, tampasFormadas, ladosPecas, ladosChao, ladosParede]
                infoJogada = t.calcularInfosDaJogada(board, peca, x, r, buracosTotaisAntes, tampasTotaisAntes)
                if infoJogada[0]: #jogadaValida

                    #self.pesos = [-3.78, 1.6, -2.31, -0.59, 4.0, 0.65, 6.52]

                    #calcular score do movimento
                    scoreMovimento = 0
                    for i in range(1, len(infoJogada)):
                        scoreMovimento += self.pesos[i-1]*infoJogada[i]
                    """
                    scoreMovimento = (-3.78*alturaTotal
                                      +1.6 * numLinhasCompletas
                                      - 2.31 * buracosFormados
                                      -0.59 * tampasFormadas
                                      + 4.0 * ladosPecas
                                      + 0.65 * ladosChao
                                      + 6.52 * ladosParede )
                    """
                    #atualiza o melhor movimento    
                    if scoreMovimento > melhorScore:
                        melhorScore = scoreMovimento
                        melhorX = x
                        melhorR = r
                        melhorY = peca['y'] #p ir mais rapido
                        
        if jogoRapido:
            peca['y'] = melhorY
        else:
            peca['y'] = -2
        peca['x'] = melhorX
        peca['rotation'] = melhorR
        #print(melhorX,"   ", melhorR)
        return melhorX, melhorR


    
#########################################################################################

### A classe Geracao recebe o numero de individuos necessarios (numInd)
### e o numero de neuronios na primeira camada (numPesos) na primeira inicializacao.
### Ela tambem implementa as formas de modificacao de pesos utilizadas para se encontrar
### uma solucao satisfatoria, que no caso e' utilizando AG. Assim existem as funcoes
### que fazem a selecao, reproducao, a mutacao de bits do codigo e o Crossing Over.

class Geracao:
    #recebe uma lista de individuos

    ### ------------------ __init__ :
    ## Realiza a inicializacao dos pesos a partir das grandezas contidas nas variaveis numInd e numPesos.
    ## Cria um vetor de numPesos casas cujos valores iniciais sao randomicos distribuidos no intervalo
    ## de [-1,1].

    def __init__ (self, numInd, numPesos=7):
        #gerar geracao0
        individuos = []

        for k1 in range(numInd):
            pesos0 = numPesos*[0]
            for k2 in range (0,numPesos):
                pesos0[k2] = 2*random.random()-1

            indiv = Individuo(pesos0)
            individuos.append(indiv)
            
        self.individuos = individuos

    def __str__(self):
        #nao precisa mexer aqui
        #retorna o print do individuo facil de ler
        for i in range(len(self.individuos)):
            print("Individuo %d:"%i)
            print(self.individuos[i])
        return ''

    ### ---------------------- selecao:
    ## Realiza a selecao dos numSelec melhor individuos baseados no score de uma simulacao do jogo.
    ## Ordena os individuos baseados nos scores e seleciona os numSelec melhores.
    ## COMPLETE AQUI:
    def selecao(self, numSelec):
        #seleciona os melhores ja baseado nos scores
        #COMPARA TODOS OS INDIVIDUOS E MANTEM OS numSelec MELHORES
        
        self.individuos = sorted(self.individuos, key=lambda x: x.score, reverse=True)
        totalScore = 0
        pop = len(self.individuos)
        print("");
        for i in range(pop):
            print(self.individuos[i].score, end=" ")
            totalScore += self.individuos[i].score
        print("\n Score Médio: ", totalScore / pop)
        print("melhor Score: ", self.individuos[pop-1], "\n")
        self.individuos = self.individuos[:numSelec]

        return self

    ### ----------------------- reproduzir:
    ## A partir dos individuos selecionados em 'selecao' com melhor score, duplica os individuos
    ## comecando pelo de melhor score ate o numero de individuos chegar ao valor da variavel 'm'.
    ## Cuidado aqui: se 'm' for maior que o dobro do numero de individuos, qual individuo sera
    ## copiado para ser o individuo m+1?

    ## Realiza o Crossing Over e a Mutacao nos individuos novos gerados.

    ## COMPLETE AQUI:
    def reproduzir(self, m, chanceCO = 0.5, chanceMut = 0.15):
        #TRANSFORMA UMA GERACAO DE n (=len(self.individuos)) INDIVIDUOS EM UMA GERACAO DE m INDIVIDUOS
        #MANTEM-SE OS INDIVIDUOS SELECIONADOS (COM SCORE JA CONHECIDO!!! - NAO NECESSARIO RETESTAR)
        #ADICIONA-SE INDIVIDUOS NOVOS BASEADOS EM VARIACOES DESSES JA SELECIONADOS ATRAVES DE:
        ##  CROSSING-OVERS
        ##  MUTACOES

        n = len(self.individuos)

        #AUMENTANDO O NUMERO DE INDIVIDUOS SEM VARIACOES
        k = 0
        while len(self.individuos) < m :
            
            pesos = self.individuos[k].pesos[:]
            individuo1 = Individuo(pesos)
            pesos = self.individuos[k+1].pesos[:]
            individuo2 = Individuo(pesos)

            self.genCrossOver(individuo1,individuo2,chanceCO)
            self.genMut(individuo1,chanceMut)
            self.genMut(individuo2,chanceMut)
            
            self.individuos.append(individuo1)
            
            if len(self.individuos) < m:
                self.individuos.append(individuo2)
                
            k += 2

        return self

    ### --------------------- genCrossOver:
    ## Aplica o crossing over 'numCO' vezes na duplicacao de cada individuo gerada por reproduzir.
    ## Seleciona randomicamente uma das casas do vetor de peso do individuo[0] (que e' o individuo
    ## com maior score - vale a reflexao: porque? -), seleciona dois individuos daqueles duplicados
    ## e troca entre eles os valores do peso daquela casa em seu vetor de pesos.
    ## COMPLETE AQUI:
    def genCrossOver(self, individuo1, individuo2, chanceCO):
        for k in range (len(individuo1.pesos)):
            r = random.random()
            if r < chanceCO:
                individuo1.pesos[k], individuo2.pesos[k] = individuo2.pesos[k], individuo1.pesos[k]



    ### ----------------------- genMut:
    ## Para um 'numMut' de vezes, seleciona uma das casas do vetor de peso de um dos
    ## individuos duplicados e modifica o valor do peso daquela casa multiplicando-o
    ## por um numero randomico entre [-1,1].

    ## Vale a reflexao: quantos valores diferentes esse numero randomico pode assumir
    ## dentro do intervalo de [-1,1]?
    ## COMPLETE AQUI:
    def genMut(self, individuo1, chanceMut):
        for k1 in range (len(individuo1.pesos)):
            r = random.random()
            if r < chanceMut:                
                #realizando a mutacao
                mut = 10 + individuo1.pesos[k1]/10.0                   #mut eh um parametro relaxionado com a dispersao possivel de mutacao
                individuo1.pesos[k1] += mut*(2*random.randrange(1000)/1000.0 - 1)       #randomicamente adiciona-se algo entre +- mut no gene

