import pygame
import neat
import math
import random
import sys

WIN_WIDTH = 1500
WIN_HEIGHT = 800


class Car:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load("img/car.png"), (100,100))
        self.rotate_img = self.img
        self.position = [700,650]
        self.centre = [self.position[0] + 50, self.position[1] + 50]
        self.angle = 0
        self.vitesse = 0
        self.sensors = []
        self.alive = True
        self.distance = 0
        self.time = 0

    def draw(self, win):
        win.blit(self.rotate_img, self.position)
        self.draw_sensors(win)

    def draw_sensors(self, win):
        for i in self.sensors:
            position, distance = i
            pygame.draw.line(win, (255,0,0), self.centre, position, width=1)
            pygame.draw.circle(win, (255,0,0), position, 5)

    def check_sensors(self, angle_degree, circuit):
        len = 0
        x = int(self.centre[0] + math.cos(math.radians(360 - (self.angle + angle_degree))) * len)
        y = int(self.centre[1] + math.sin(math.radians(360 - (self.angle + angle_degree))) * len)

        while not circuit.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = int(self.centre[0] + math.cos(math.radians(360 - (self.angle + angle_degree))) * len)
            y = int(self.centre[1] + math.sin(math.radians(360 - (self.angle + angle_degree))) * len)

        dist = int(math.sqrt(math.pow(x - self.centre[0], 2) + math.pow(y - self.centre[1], 2)))
        self.sensors.append([(x, y), dist])

    def collide(self, circuit):
        for p in self.check_points:
            if circuit.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.alive = False
                break
    
    def update(self, circuit):
        self.speed = 15

        self.rotate_img = self.rot_center(self.img, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.vitesse
        if self.position[0] < 20:
            self.position[0] = 20
        elif self.position[0] > WIN_WIDTH - 120:
            self.position[0] = WIN_WIDTH - 120
        
        self.distance += self.speed
        self.time += 1
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        if self.position[1] < 20:
            self.position[1] = 20
        elif self.position[1] > WIN_WIDTH - 120:
            self.position[1] = WIN_HEIGHT - 120

        self.centre = [int(self.position[0]) + 50, int(self.position[1]) + 50]
        len = 40
        left_top = [self.centre[0] + math.cos(math.radians(360 - (self.angle + 30))) * len, self.centre[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.centre[0] + math.cos(math.radians(360 - (self.angle + 150))) * len, self.centre[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.centre[0] + math.cos(math.radians(360 - (self.angle + 210))) * len, self.centre[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.centre[0] + math.cos(math.radians(360 - (self.angle + 330))) * len, self.centre[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        self.check_points = [left_top, right_top, left_bottom, right_bottom]

        self.collide(circuit)
        self.sensors.clear()
        for d in range(-90, 120, 45):
            self.check_sensors(d, circuit)

    def get_data(self):
        sensors = self.sensors
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(sensors):
            ret[i] = int(r[1] / 30)

        return ret

    def get_alive(self):
        return self.is_alive

    def get_reward(self):
        return self.distance / 50.0

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image       

def main():
    pygame.init()
    circuit = pygame.image.load("img/map2.png")
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    car = Car()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        win.blit(circuit, (0, 0))
        car.update(circuit)
        car.draw(win)
        pygame.display.flip()


if __name__ == "__main__":
    main()
    
