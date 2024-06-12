import pygame  

LARGURA, ALTURA = 900, 500
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini-GuitarHero")
FPS = 60

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()



if __name__ == "__main__":  #FAZ COM QUE SÓ ABRA O PROGRAMA ATRAVÉS DO ARQUIVO MAIN
    main()
