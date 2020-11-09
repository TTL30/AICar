import pygame, neat
import sys, os
from car import Car

WIN_WIDTH = 1500
WIN_HEIGHT = 800
CIRCUIT_IMG = pygame.image.load("img/map2.png")
pygame.init()


def nn(genomes, config):

    nets = []
    cars = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    circuit = CIRCUIT_IMG

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

        pygame.display.flip()
        clock.tick(0)

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
