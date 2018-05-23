#encoding: utf
import sys
import time

#Tempo inicial
time_i = time.time()

class Tab:
    # Representa o Tabuleiro do Resta um
    
    def __init__(self):
        # Inicializa o tabuleiro
        # 0 vazio, 1 ocupado e 2 inválido
        self.table = [
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2]
        ]

    def reset(self):
        # Reinicializa o tabuleiro
        self.__init__()

    def move(self, linha, coluna, dir):
        """Verifica se existe uma peça na posição dada e se a jogada é válida

        Args:
            linha (int): linha da peça
            coluna (int): coluna da peça
            dir (int): Direção do movimento. 0 (esquerda), 1 (direita), 2 (cima), 3 (baixo)

        Se o movimento é válido devolve True, se não devolve False"""

        if self.table[linha][coluna] != 1:
            return False

        if dir == 0 and coluna-2 >= 0\
                    and self.table[linha][coluna-1] == 1\
                    and self.table[linha][coluna-2] == 0:
            self.table[linha][coluna] = self.table[linha][coluna-1] = 0
            self.table[linha][coluna-2] = 1

            return True

        if dir == 1 and coluna+2 < len(self.table[0]) \
                    and self.table[linha][coluna+1] == 1 \
                    and self.table[linha][coluna+2] == 0:
            self.table[linha][coluna] = self.table[linha][coluna+1] = 0
            self.table[linha][coluna+2] = 1

            return True

        if dir == 2 and linha-2 >= 0 \
                    and self.table[linha-1][coluna] == 1 \
                    and self.table[linha-2][coluna] == 0:
            self.table[linha][coluna] = self.table[linha-1][coluna] = 0
            self.table[linha-2][coluna] = 1

            return True

        if dir == 3 and linha+2 < len(self.table) \
                    and self.table[linha+1][coluna] == 1 \
                    and self.table[linha + 2][coluna] == 0:
            self.table[linha][coluna] = self.table[linha+1][coluna]  = 0
            self.table[linha+2][coluna] = 1

            return True

        return False

    def unmove(self, linha, coluna, dir):
        #Volta a posição anterior do pino movimentado 

        if dir == 0:
            self.table[linha][coluna] = self.table[linha][coluna-1] = 1
            self.table[linha][coluna-2] = 0
            return

        if dir == 1:
            self.table[linha][coluna] = self.table[linha][coluna+1] = 1
            self.table[linha][coluna+2] = 0
            return

        if dir == 2:
            self.table[linha][coluna] = self.table[linha-1][coluna] = 1
            self.table[linha-2][coluna] = 0

        if dir == 3:
            self.table[linha][coluna] = self.table[linha+1][coluna] = 1
            self.table[linha+2][coluna] = 0

    def showtab(self):
        #Imprime o tabuleiro na tela

        char_map = {
            2: ' x ',
            0: '   ',
            1: ' i '
        }

        linhas = len(self.table)
        colunas = len(self.table[0])

        sys.stdout.write('  ')
        for coluna in xrange(colunas):
            sys.stdout.write(' {0} '.format(str(coluna)))

        sys.stdout.write('\n')

        for linha in xrange(linhas):
            for coluna in xrange(colunas):
                if coluna == 0:
                    sys.stdout.write('{0} '.format(str(linha)))

                sys.stdout.write('{0}'.format(char_map[self.table[linha][coluna]]))

                if coluna == colunas-1:
                    sys.stdout.write(' \n')


class TabSolver:
    def __init__(self, tab):
        """Recebe o Tabuleiro como parâmetro
        
        Retorna:
            Solução

        """
        self.tab = tab

        num_pinos = 0
        for linha in self.tab.table:
            for elem in linha:
                if elem == 1:
                    num_pinos += 1

        # Número máximo de movimentos
        self.max_moves = num_pinos - 1

        # Centro do Tabuleiro
        self.center_linha = len(self.tab.table) / 2
        self.center_coluna = len(self.tab.table[0]) / 2

        self.solution = []
        self.test = []

    def _back_track(self, move):
        """Verifica se a solução existe
            Retorna True caso a solução exista
        """
        if move == self.max_moves:
            # Verifica se restou um pino na posição central no fim das jogadas
            if self.tab.table[self.center_linha][self.center_coluna] == 1:
                return True
            else:
                return False

        # Passando pelas posições do tabuleiro
        for r in xrange(len(self.tab.table)):
            for c in xrange(len(self.tab.table[0])):
                # Tenta movimentar em alguma direção
                for d in xrange(4):
                    # Verifica se o movimento é válido
                    if self.tab.move(r, c, d):
                        # Verifica se o caminho possui a solução
                        if self._back_track(move + 1):
                            # Salva a jogada se a solução foi encontrada
                            self.solution.append((r, c, d))
                            return True

                        # Volta caso a solução não tenha sido encontrada
                        self.tab.unmove(r, c, d)
                        # Salva as tentativas de jogadas
                        self.test.append((r,c,d))

        return False

    def solve(self):
        """Encontra os movimentos necessários para ganhar o jogo

        Retorna:
            Uma lista contendo a posição do pino e a direção que foi movimentado

        """
        print '\n Estamos calculando a solução, aguarde...'
        # Reseta o tabuleiro e a lista de soluções
        self.solution = []
        self.tab.reset()
        # Inicia o backtracking
        self._back_track(0)
        
        # Ajusta a solução na ordem correta
        self.solution.reverse()

        return self.solution

    def print_solution(self):
        #Imprime a solução passo a passo com  
        self.tab.reset()

        print '\nTabuleiro Inicial\n'
        self.tab.showtab()

        dir_map = {
            0: 'esquerda',
            1: 'direita',
            2: 'cima',
            3: 'baixo'
        }

        for step in self.solution:
            r, c, d = step

            print '\nMovimento: linha {0} coluna {1} {2}\n'.format(r, c, dir_map[d])

            self.tab.move(*step)
            self.tab.showtab()
        
        print "O número de tentativas foi de {}\n".format(len(self.test))


if __name__ == '__main__':
    
    t = TabSolver(Tab())
    t.solve()

t.print_solution()
print "Tempo de execução: {}".format(time.time()-time_i)
