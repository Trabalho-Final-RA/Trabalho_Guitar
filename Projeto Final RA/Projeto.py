import pygame
import os
import random

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da tela
LARGURA, ALTURA = 900, 500
LARGURA_GUITARRA = 450
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini-GuitarHero")
FPS = 60

# Inicializar fontes
pygame.font.init()

# Carregar e redimensionar imagens
FUNDO = pygame.image.load(os.path.join('Imagens', 'fundo.png'))
FUNDO = pygame.transform.scale(FUNDO, (LARGURA, ALTURA))
NOTA_MUSICAL = pygame.image.load(os.path.join('Imagens', 'bola.png'))
NOTA_MUSICAL_AJUSTADA = pygame.transform.scale(NOTA_MUSICAL, (70, 70))
play_img = pygame.image.load(os.path.join('Imagens', 'Start.png')).convert_alpha()
exit_img = pygame.image.load(os.path.join('Imagens', 'Exit.png')).convert_alpha()
back_img = pygame.image.load(os.path.join('Imagens', 'resume.png')).convert_alpha()

# Definir cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Definir constantes
VELOCIDADE_NOTA = 5
DURACAO_CRIACAO_NOTAS = 168000  # 168 segundos em milissegundos
INTERVALO_CRIACAO_NOTAS = 500  # 0,5 segundos em milissegundos

class NotaMusical:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = NOTA_MUSICAL_AJUSTADA

    def desenhar(self, WIN):
        WIN.blit(self.image, (self.x, self.y))

    def mover(self):
        self.y += VELOCIDADE_NOTA

class Button:
    def __init__(self, x, y, image, scale):
        largura = image.get_width()
        altura = image.get_height()
        self.image = pygame.transform.scale(image, (int(largura * scale), int(altura * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

play_botao = Button(90, 200, play_img, 0.5)
exit_botao = Button(500, 200, exit_img, 0.5)
back_botao = Button(300, 300, back_img, 0.5)

def desenhar_linhas_divisao():
    um_quarto_largura = LARGURA_GUITARRA // 4
    linha_horizontal_y = ALTURA // 2 + 100
    deslocamento_x = (LARGURA - LARGURA_GUITARRA) // 2

    for i in range(5):
        x = deslocamento_x + i * um_quarto_largura
        pygame.draw.line(WIN, BRANCO, (x, 0), (x, ALTURA), 2)

    pygame.draw.line(WIN, BRANCO, (deslocamento_x, linha_horizontal_y), (deslocamento_x + LARGURA_GUITARRA, linha_horizontal_y), 2)

def desenhar_texto(texto, x, y, tamanho):
    fonte = pygame.font.SysFont('Arial', tamanho)
    superficie_texto = fonte.render(texto, True, BRANCO)
    WIN.blit(superficie_texto, (x, y))

def desenhar(notas, contador, erros):
    WIN.blit(FUNDO, (0, 0))
    desenhar_linhas_divisao()
    for nota in notas:
        nota.desenhar(WIN)
    desenhar_texto(f"Contador: {contador}", 50, 100, 25)
    desenhar_texto(f"Erros: {erros}", 50, 150, 25)
    pygame.display.update()

def calcular_porcentagens(contador, erros):
    total = contador + erros
    if total == 0:
        return 0, 0
    porcentagem_acertos = (contador / total) * 100
    porcentagem_erros = (erros / total) * 100
    return porcentagem_acertos, porcentagem_erros

def verificar_colisao(notas, contador, quadrante):
    um_quarto_largura = LARGURA_GUITARRA // 4
    deslocamento_x = (LARGURA - LARGURA_GUITARRA) // 2
    quadrante_x_min = deslocamento_x + quadrante * um_quarto_largura
    quadrante_x_max = quadrante_x_min + um_quarto_largura
    quadrante_y_min = ALTURA // 2 + 100
    quadrante_y_max = quadrante_y_min + 150
    erro = 1

    for nota in notas:
        if (quadrante_x_min <= nota.x <= quadrante_x_max and
            quadrante_y_min <= nota.y + NOTA_MUSICAL_AJUSTADA.get_height() // 2 <= quadrante_y_max):
            contador += 1
            notas.remove(nota)
            erro = 0
            break
    return contador, erro

def show_victory_screen(contador, erros):
    porcentagem_acertos, porcentagem_erros = calcular_porcentagens(contador, erros)
    WIN.fill(PRETO)
    font = pygame.font.Font(None, 74)
    text = font.render("Créditos:\nAshley martins \nJoão Vitor de Moraes Bringmann \nMatheus Becchi Arruda \nFIM!", True, BRANCO)
    WIN.blit(text, (LARGURA // 2 - text.get_width() // 2, ALTURA // 2 - text.get_height() // 2))

    desenhar_texto(f"Acertos: {porcentagem_acertos:.2f}%", 50, 300, 25)
    desenhar_texto(f"Erros: {porcentagem_erros:.2f}%", 50, 350, 25)

    if back_botao.draw(WIN):
        return "main_menu"

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    run = True
    contador = 0
    erros = 0
    notas = []
    inicio_tempo = pygame.time.get_ticks()
    ultimo_tempo_criacao = inicio_tempo
    deslocamento_x = (LARGURA - LARGURA_GUITARRA) // 2
    musica_tocando = False
    musica_terminada = False
    estado = "main_menu"  # Adicione um estado para gerenciar a tela atual

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if musica_tocando and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    contador, erro = verificar_colisao(notas, contador, 0)
                    erros += erro
                elif event.key == pygame.K_DOWN:
                    contador, erro = verificar_colisao(notas, contador, 1)
                    erros += erro
                elif event.key == pygame.K_UP:
                    contador, erro = verificar_colisao(notas, contador, 2)
                    erros += erro
                elif event.key == pygame.K_RIGHT:
                    contador, erro = verificar_colisao(notas, contador, 3)
                    erros += erro
                else:
                    erros += 1

        WIN.fill(PRETO)

        if estado == "main_menu":
            if play_botao.draw(WIN) and not musica_tocando:
                pygame.mixer.music.load(os.path.join('music2.mp3'))
                pygame.mixer.music.play()
                musica_tocando = True
                estado = "playing"

            if exit_botao.draw(WIN):
                run = False

        elif estado == "playing":
            tempo_atual = pygame.time.get_ticks()
            tempo_decorrido = tempo_atual - inicio_tempo

            if tempo_decorrido < DURACAO_CRIACAO_NOTAS and tempo_atual - ultimo_tempo_criacao >= INTERVALO_CRIACAO_NOTAS:
                coluna = random.randint(0, 3)
                x = deslocamento_x + coluna * (LARGURA_GUITARRA // 4) + (LARGURA_GUITARRA // 8) - NOTA_MUSICAL_AJUSTADA.get_width() // 2
                y = 0
                notas.append(NotaMusical(x, y))
                ultimo_tempo_criacao = tempo_atual

            for nota in notas:
                nota.mover()

            desenhar(notas, contador, erros)

            if not pygame.mixer.music.get_busy():
                musica_terminada = True
                musica_tocando = False
                estado = "victory"

        elif estado == "victory":
            result = show_victory_screen(contador, erros)
            if result == "main_menu":
                estado = "main_menu"
                contador = 0
                erros = 0
                notas = []
                musica_terminada = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()