import sys
import pygame
from pygame.locals import *
from constante import *
from math import *
import math
from PIL import Image
import numpy as np
from random import randrange
from collections import defaultdict 
import itertools



vec = pygame.math.Vector2


class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((26, 45), pygame.SRCALPHA)
        self.haut = pygame.image.load("img/car.png").convert()
        self.haut.set_colorkey((0,0,0))
        self.image.blit(self.haut,(0,0))
        self.original_image = self.image

        class etat:
            position = vec(275, 295)
            distCapt=[1000,1000,1000,1000,1000]

        self.state=etat
        self.rect = self.image.get_rect(center=self.state.position)
        self.vel = vec(0, 0)
        self.heading = vec(0, -1)  # upwards
        self.acceleration = vec(0, -0.1)  # The acceleration vec points upwards.
        self.angle_speed = 0
        self.angle = 0
        self.angleCapt = 90
        self.sensor1 = [275, 295]
        self.sensor2 = [275, 295]
        self.sensor3 = [275, 275]
        self.sensor4 = [275, 275]
        self.sensor5 = [275, 275]
        
       

    def movements(self,action):
        ACTION_UP = 0
        ACTION_LEFT = 1
        ACTION_DOWN = 2
        ACTION_RIGHT = 3
        ACTIONS = [ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_UP]
        ACTION_NAMES = ["UP", "LEFT", "DOWN", "RIGHT"]
        if action==ACTION_LEFT :
            self.angle_speed = -2
            Car.rotate(self)
            self.vel += self.acceleration
        if action==ACTION_RIGHT :
            self.angle_speed = 2
            Car.rotate(self)
            self.vel += self.acceleration
        if action==ACTION_UP :
            self.vel += self.acceleration  
        if action==ACTION_DOWN:
            self.vel -= self.acceleration

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle_speed = -2
            Car.rotate(self)
            self.vel += self.acceleration

        if keys[K_RIGHT]:
            self.angle_speed = 2
            Car.rotate(self)
            self.vel += self.acceleration

        if keys[K_UP]:
            self.vel += self.acceleration

        if keys[K_DOWN]:
            self.vel -= self.acceleration

        # max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.state.position += self.vel
        self.rect.center = self.state.position

    def collisionMurs(self):
        if(self.state.distCapt[0]<22 or self.state.distCapt[1]<13 or self.state.distCapt[2]<13 or self.state.distCapt[3]<18 or self.state.distCapt[4]<18):
            self.__init__()

    def calculdistance(self):
        #Capt1
        disYC1_1=self.sensor1[1]-self.state.position[1]
        disYC1=disYC1_1*disYC1_1
        disXC1_1=self.sensor1[0]-self.state.position[0]
        disXC1=disXC1_1*disXC1_1
        self.state.distCapt[0]=sqrt(disXC1+disYC1)
        #Capt2
        disYC2_1=self.sensor2[1]-self.state.position[1]
        disYC2=disYC2_1*disYC2_1
        disXC2_1=self.sensor2[0]-self.state.position[0]
        disXC2=disXC2_1*disXC2_1
        self.state.distCapt[1]=sqrt(disXC2+disYC2)

        #Capt3
        disYC3_1=self.sensor3[1]-self.state.position[1]
        disYC3=disYC3_1*disYC3_1
        disXC3_1=self.sensor3[0]-self.state.position[0]
        disXC3=disXC3_1*disXC3_1
        self.state.distCapt[2]=sqrt(disXC3+disYC3)
        #Capt4
        disYC4_1=self.sensor4[1]-self.state.position[1]
        disYC4=disYC4_1*disYC4_1
        disXC4_1=self.sensor4[0]-self.state.position[0]
        disXC4=disXC4_1*disXC4_1
        self.state.distCapt[3]=sqrt(disXC4+disYC4)
        #Capt5
        disYC5_1=self.sensor5[1]-self.state.position[1]
        disYC5=disYC5_1*disYC5_1
        disXC5_1=self.sensor5[0]-self.state.position[0]
        disXC5=disXC5_1*disXC5_1
        self.state.distCapt[4]=sqrt(disXC5+disYC5)

    def rotate(self):
        # Rotate the acceleration vector.
        if(self.angle_speed<0):
            self.acceleration.rotate_ip(self.angle_speed)
        else :
            self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        self.angleCapt -= self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def CalculVectorsCapteurs(self,circuit):
        #Capteur 1
        scale=1
        self.sensor1[0]=math.cos(math.radians(-self.angleCapt))*scale + self.state.position[0]
        self.sensor1[1]=math.sin(math.radians(-self.angleCapt))*scale + self.state.position[1]
        while(circuit[int(self.sensor1[0]),int(self.sensor1[1])]== 1):
            scale+=1
            self.sensor1[0]=math.cos(math.radians(-self.angleCapt))*scale + self.state.position[0]
            self.sensor1[1]=math.sin(math.radians(-self.angleCapt))*scale + self.state.position[1]

        #Capteur 2
        scale2=1
        self.sensor2[0]=math.cos(math.radians(-self.angleCapt+90))*scale2 + self.state.position[0]
        self.sensor2[1]=math.sin(math.radians(-self.angleCapt+90))*scale2 + self.state.position[1]

        while(circuit[int(self.sensor2[0]),int(self.sensor2[1])]== 1):
            scale2+=1
            
            self.sensor2[0]=math.cos(math.radians(-self.angleCapt+90))*scale2 + self.state.position[0]
            self.sensor2[1]=math.sin(math.radians(-self.angleCapt+90))*scale2 + self.state.position[1]

        #Capteur 3
        scale3=1
        self.sensor3[0]=math.cos(math.radians(-self.angleCapt-90))*scale3 + self.state.position[0]
        self.sensor3[1]=math.sin(math.radians(-self.angleCapt-90))*scale3 + self.state.position[1]

        while(circuit[int(self.sensor3[0]),int(self.sensor3[1])]== 1):
            scale3+=1
            self.sensor3[0]=math.cos(math.radians(-self.angleCapt-90))*scale3 + self.state.position[0]
            self.sensor3[1]=math.sin(math.radians(-self.angleCapt-90))*scale3 + self.state.position[1]

        #Capteur 4
        scale4=1
        self.sensor4[0]=math.cos(math.radians(-self.angleCapt-45))*scale4 + self.state.position[0]
        self.sensor4[1]=math.sin(math.radians(-self.angleCapt-45))*scale4 + self.state.position[1]

        while(circuit[int(self.sensor4[0]),int(self.sensor4[1])]== 1):
            scale4+=1
            self.sensor4[0]=math.cos(math.radians(-self.angleCapt-45))*scale4 + self.state.position[0]
            self.sensor4[1]=math.sin(math.radians(-self.angleCapt-45))*scale4 + self.state.position[1]

        #Capteur 5
        scale5=1
        self.sensor5[0]=math.cos(math.radians(-self.angleCapt+45))*scale5 + self.state.position[0]
        self.sensor5[1]=math.sin(math.radians(-self.angleCapt+45))*scale5 + self.state.position[1]

        while(circuit[int(self.sensor5[0]),int(self.sensor5[1])]== 1):
            scale5+=1
            self.sensor5[0]=math.cos(math.radians(-self.angleCapt+45))*scale5 + self.state.position[0]
            self.sensor5[1]=math.sin(math.radians(-self.angleCapt+45))*scale5 + self.state.position[1]
       
    def draw_vectors(self, screen):
        scale = 20
        # vel
        pygame.draw.line(screen, GREEN, self.state.position, (self.state.position + self.vel * scale), 5)
        # capteurs
        pygame.draw.line(screen,RED,self.state.position,self.sensor1,1)
        pygame.draw.line(screen,BLUE,self.state.position,self.sensor2,1)
        pygame.draw.line(screen,BLUE,self.state.position,self.sensor3,1)
        pygame.draw.line(screen,GREEN,self.state.position,self.sensor4,1)
        pygame.draw.line(screen,GREEN,self.state.position,self.sensor5,1)
        # intersections points
        pygame.draw.ellipse(screen,BLACK,(int(self.sensor1[0])-3,int(self.sensor1[1]),8,8))
        pygame.draw.ellipse(screen,BLACK,(int(self.sensor2[0])-3,int(self.sensor2[1]),8,8))
        pygame.draw.ellipse(screen,BLACK,(int(self.sensor3[0])-3,int(self.sensor3[1]),8,8))
        pygame.draw.ellipse(screen,BLACK,(int(self.sensor4[0])-3,int(self.sensor4[1]),8,8))
        pygame.draw.ellipse(screen,BLACK,(int(self.sensor5[0])-3,int(self.sensor5[1]),8,8))
     
    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.state.position.x > WIDTH:
            self.state.position.x = 0
        if self.state.position.x < 0:
            self.state.position.x = WIDTH
        if self.state.position.y <= 0:
            self.state.position.y = HEIGHT
        if self.state.position.y > HEIGHT:
            self.state.position.y = 0


    def learningCar(self):
        Left=0
        Right=1
        Up=2
        Down=3
        direc = np.zeros([10], int)
        for i in range (10):
            direc[i]=randrange(4)

        for j in range (10):
            if direc[j]==Left:
                self.angle_speed = -1
                Car.rotate(self)
                self.vel += self.acceleration
                

            if direc[j]==Right:
                self.angle_speed = 1
                Car.rotate(self)
                self.vel += self.acceleration

            if direc[j]==Up:
                self.vel += self.acceleration
            if direc[j]==Down:
                self.vel -= self.acceleration

            # max speed
            if self.vel.length() > MAX_SPEED:
                self.vel.scale_to_length(MAX_SPEED)

            self.state.position += self.vel
            self.rect.center = self.state.position


    



   