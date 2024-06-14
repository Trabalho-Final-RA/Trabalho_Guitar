import pygame
import os  # Sistema de operação do computador para ajudar a puxar imagens
import random

LARGURA, ALTURA = 900, 500
LARGURA_GUITARRA = 450
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini-GuitarHero")
FPS = 60

# Inicializar o Pygame e o módulo de fontes
pygame.init()
pygame.font.init()

# Carregar e ajustar a imagem da nota musical
NOTA_MUSICAL = pygame.image.load(os.path.join('Imagens', 'Nota_musical.png'))
NOTA_MUSICAL_AJUSTADA = pygame.transform.scale(NOTA_MUSICAL, (70, 70))

BRANCO = (255, 255, 255)
BLACK = (0, 0, 0)
VELOCIDADE_NOTA = 5
DURACAO_CRIACAO_NOTAS = 100000  # 100 segundos em milissegundos
INTERVALO_CRIACAO_NOTAS = 2000  # 2 segundos em milissegundos

class NotaMusical:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = NOTA_MUSICAL_AJUSTADA

    def desenhar(self, WIN):
        WIN.blit(self.image, (self.x, self.y))

    def mover(self):
        self.y += VELOCIDADE_NOTA

def desenhar_linhas_divisao():
    um_quarto_largura = LARGURA_GUITARRA // 4
    linha_horizontal_y = ALTURA // 2 + 100  # Linha um pouco abaixo da metade da tela

    # Calcula o deslocamento para centralizar a guitarra
    deslocamento_x = (LARGURA - LARGURA_GUITARRA) // 2

    # Linhas verticais
    for i in range(5):  # De 0 a 4 para desenhar quatro linhas dentro da guitarra e uma em cada borda
        x = deslocamento_x + i * um_quarto_largura
        pygame.draw.line(WIN, BRANCO, (x, 0), (x, ALTURA), 2)  # 2 é a largura da linha

    # Linha horizontal
    pygame.draw.line(WIN, BRANCO, (deslocamento_x, linha_horizontal_y), (deslocamento_x + LARGURA_GUITARRA, linha_horizontal_y), 2)  # 2 é a largura da linha

def desenhar_texto(texto, x, y, tamanho):
    fonte = pygame.font.SysFont('Arial', tamanho)
    superficie_texto = fonte.render(texto, True, BRANCO)
    WIN.blit(superficie_texto, (x, y))

def desenhar(notas, contador, erros):
    WIN.fill((BLACK))  # Preenchendo a tela
    desenhar_linhas_divisao()
    for nota in notas:
        nota.desenhar(WIN)
    desenhar_texto(f"Acertos: {contador}", 50, 100, 25)  # Desenhar o texto após desenhar as notas e linhas
    desenhar_texto(f"Erros: {erros}", 50, 150, 25)
    pygame.display.update()  # Atualizando a tela

def verificar_colisao(notas, contador, quadrante):
    # Definir o retângulo do quadrante
    um_quarto_largura = LARGURA_GUITARRA // 4
    deslocamento_x = (LARGURA - LARGURA_GUITARRA) // 2
    quadrante_x_min = deslocamento_x + quadrante * um_quarto_largura
    quadrante_x_max = quadrante_x_min + um_quarto_largura
    quadrante_y_min = ALTURA // 2 + 100
    quadrante_y_max = quadrante_y_min + 150  # Altura da imagem da nota musical
    erro = 1  # Assume que é um erro por padrão

    # Verificar se alguma nota está dentro do quadrante
    for nota in notas:
        if (quadrante_x_min <= nota.x <= quadrante_x_max and
            quadrante_y_min <= nota.y + NOTA_MUSICAL_AJUSTADA.get_height() // 2 <= quadrante_y_max):
            contador += 1
            notas.remove(nota)
            erro = 0  # Não é um erro se a nota for acertada
            break
    return contador, erro

def main():
    clock = pygame.time.Clock()
    run = True
    contador = 0
    erros = 0

    # Lista para armazenar as notas musicais
    notas = []

    inicio_tempo = pygame.time.get_ticks()
    ultimo_tempo_criacao = inicio_tempo

    # Calcula o deslocamento para centralizar a guitarra
    deslocamento_x = (LARGURA - LARGURA_GUITARRA) // 2

    while run:
        clock.tick(FPS)
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = tempo_atual - inicio_tempo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    contador, erro = verificar_colisao(notas, contador, 0)
                    erros += erro
                elif event.key == pygame.K_s:
                    contador, erro = verificar_colisao(notas, contador, 1)
                    erros += erro
                elif event.key == pygame.K_d:
                    contador, erro = verificar_colisao(notas, contador, 2)
                    erros += erro
                elif event.key == pygame.K_f:
                    contador, erro = verificar_colisao(notas, contador, 3)
                    erros += erro

        if tempo_decorrido < DURACAO_CRIACAO_NOTAS and tempo_atual - ultimo_tempo_criacao >= INTERVALO_CRIACAO_NOTAS:
            # Criar nova nota musical a cada 2 segundos durante os primeiros 100 segundos
            coluna = random.randint(0, 3)
            x = deslocamento_x + coluna * (LARGURA_GUITARRA // 4) + (LARGURA_GUITARRA // 8) - NOTA_MUSICAL_AJUSTADA.get_width() // 2
            y = 0
            notas.append(NotaMusical(x, y))
            ultimo_tempo_criacao = tempo_atual

        for nota in notas:
            nota.mover()

        desenhar(notas, contador, erros)  # Chamando desenhar no final para garantir que o texto não seja sobrescrito

    pygame.quit()

if __name__ == "__main__":
    main()
