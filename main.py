import pygame
import os #sistema de operação do computador para ajudar a puxar imagens

LARGURA, ALTURA = 900, 500
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini-GuitarHero")
FPS = 60
NOTA_MUSICAL = pygame.image.load(os.path.join('Imagens', 'Nota_musical.png'))
NOTA_MUSICAL_AJUSTADA = pygame.transform.scale(NOTA_MUSICAL, (50, 50))

BRANCO = (255, 255, 255)

def desenhar_linhas_divisao():
    um_quarto_largura = LARGURA // 4
    for i in range(1, 4):  # De 1 a 3 para desenhar três linhas
        x = i * um_quarto_largura
        pygame.draw.line(WIN, BRANCO, (x, 0), (x, ALTURA), 2)  # 2 é a largura da linha

def desenhar():
    WIN.fill((0, 0, 0))  # Preenchendo a tela
    desenhar_linhas_divisao()
    WIN.blit(NOTA_MUSICAL_AJUSTADA, (100, 100))
    pygame.display.update()   # Atualizando a tela



def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        desenhar()

    pygame.quit()

if __name__ == "__main__":
    main()
