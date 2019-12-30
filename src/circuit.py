import time
import pygame
from pygame.locals import *
import numpy as np
from PIL import Image

def CreationVisuelCircuit():
    # Chargement et collage de la surface
    surface = pygame.Surface((1300, 600))
    surface = surface.convert()
    surface.fill((250,250,250))
    #chargement image
    circuitIMG = pygame.image.load("img/circuit.png").convert()
    #Affichage surface fond
    surface.blit(circuitIMG,(0,0))
    return surface
    
def CreationTabCircuit(surface):
    #init tab circuit
    circuit = np.zeros([1300, 600], int)
    #creation tab circuit
    for i in range (1300):
        for j in range (600):
            pix=surface.get_at((i,j))
            if(pix==(91,155,213,255)):
                circuit [i,j]=1
            else:
                circuit [i,j]=0
    return circuit
