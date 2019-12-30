import sys
import pygame
from pygame.locals import *
from constante import *
from car import *
from circuit import *


def main():
    #init pygame
    pygame.init()
    #init imgpersec
    fps_clock = pygame.time.Clock()
    #Creation screen
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    # Creation visuel du circuit
    surface = CreationVisuelCircuit()
    # Creation Tab valeur circuit
    moncircuit = CreationTabCircuit(surface)

    #group sprites
    all_sprites = pygame.sprite.Group()
    #Decla voiture
    carIA = Car()
    all_sprites.add(carIA)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        #Sortie ecran
        carIA.wrap_around_screen()
        #updatesprite
        #all_sprites.update()
        carIA.learningCar()
        #affichage screen
        DISPLAY.fill(BLACK)
        DISPLAY.blit(surface,(0,0))
        all_sprites.draw(DISPLAY)
    
        #vecteurs accel
        carIA.CalculVectorsCapteurs(moncircuit)
        carIA.calculdistance()
        carIA.draw_vectors(DISPLAY)
        carIA.collisionMurs()
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()