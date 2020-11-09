import pygame
import math
import sys

WIN_WIDTH = 1500
WIN_HEIGHT = 800
CAR_IMG = pygame.image.load("img/car2.png")
color = (255,255,255,255)


class Car:
    def __init__(self):
        self.img = pygame.transform.scale(CAR_IMG, (100,100))
        self.position = [750,650]
        self.speed = 0
        self.angle = 0
        self.sensors = []
        self.center = [self.position[0] + 50, self.position[1] + 50]
        self.collison_points = []
        self.alive = True
        self.rotate_img = self.img
        self.dist_parcou = 0

    def draw(self, win):
        win.blit(self.rotate_img, self.position)
        self.draw_sensors(win)
    
    def draw_sensors(self, win):
        for pos_s in self.sensors:
            pygame.draw.line(win, (255,0,0), self.center, pos_s[0], 1)
            pygame.draw.circle(win, (255,0,0), pos_s[0], 5)
        for pos_p in self.collison_points:
            pygame.draw.circle(win, (0,255,0), pos_p, 5)

    def update_coll_points(self,deg):
        long = 40
        coord = [int(self.center[0] + math.cos(math.radians(360 - (self.angle + deg))) * long), int(self.center[1] + math.sin(math.radians(360 - (self.angle + deg))) * long)]
        self.collison_points.append(coord)

    def update_sensor(self, angle, circuit):
        long = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * long)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * long)
        while not circuit.get_at((x, y)) == color:
            long += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * long)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * long)
        distance = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.sensors.append([(x, y), distance])

    def collision(self, circuit):
        for i in self.collison_points:
            if circuit.get_at((int(i[0]), int(i[1]))) == color:
                self.alive = False
                break
    
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    
    def update_center(self):
        self.center = [int(self.position[0]) + 50, int(self.position[1]) + 50]

    
    def drive(self, circuit):
        self.speed = 15
        self.dist_parcou += self.speed
        self.rotate_img = self.rot_center(self.img, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed

        self.update_center()
        
        cd = [30, 150, 210, 330]
        self.collison_points.clear()
        for i in cd:
            self.update_coll_points(i)

        self.collision(circuit)

        self.sensors.clear()
        for d in range(-90, 120, 45):
            self.update_sensor(d, circuit)

    def get_dist_sens(self):
        data = [0, 0, 0, 0, 0]
        for i, dist in enumerate(self.sensors):
            data[i] = int(dist[1])
        return data
    
    def get_status(self):
        return self.alive

    def reward(self):
        return self.dist_parcou / 50.0
