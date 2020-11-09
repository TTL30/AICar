import pygame, neat
import sys, os
from car import Car
from time import sleep
WIN_WIDTH = 1500
WIN_HEIGHT = 800
CIRCUIT_IMG = pygame.image.load("img/circuit1.png")
CIRCUIT_IMG2 = pygame.image.load("img/circuit2.png")
pygame.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
nb_gen = 0
def nn(genomes, config):

    nets = []
    cars = []
    global nb_gen

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 70)

    circuit = CIRCUIT_IMG2
    nb_gen += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_dist_sens())
            val = output.index(max(output))
            if val == 0:
                car.angle += 10
            else:
                car.angle -= 10

        still_car = 0
        for index, car in enumerate(cars):
            if car.get_status():
                still_car += 1
                car.drive(circuit)
                genomes[index][1].fitness += car.reward()

        if still_car == 0:
            break

        window.blit(CIRCUIT_IMG, (0,0))
        
        for car in cars:
            if car.get_status():
                car.draw(window)
                if(still_car == 1):
                    text = STAT_FONT.render("Distance : " + str(car.reward()), 1, (0,255,255))
                    window.blit(text, (WIN_WIDTH-50-text.get_width(),150))
        text = STAT_FONT.render("Géneration : " + str(nb_gen), 1, (0,255,255))
        window.blit(text, (WIN_WIDTH-50-text.get_width(),50))
        text = STAT_FONT.render("Cars : " + str(still_car), 1, (0,255,255))
        window.blit(text, (WIN_WIDTH-50-text.get_width(),100))

        pygame.display.flip()
        clock.tick(30)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    cr = p.run(nn,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
 