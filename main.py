import pygame
import neat
import time
import os
import random
import pickle
import matplotlib.pyplot as plt
import sys
from bird import Bird
from pipe import Pipe

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0
fitness_history = []

# Suppress all stdout (no terminal prints at all)
sys.stdout = open(os.devnull, 'w')

# Load background once
BG_IMG = pygame.image.load(os.path.join("imgs", "bg.png"))
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, birds, pipes, score, gen, paused=False):
    scaled_bg = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))
    win.blit(scaled_bg, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    gen_text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(gen_text, (10, 10))

    if paused:
        pause_text = STAT_FONT.render("PAUSED", 1, (255, 0, 0))
        win.blit(pause_text, ((WIN_WIDTH - pause_text.get_width()) // 2, WIN_HEIGHT // 2))

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        bird = Bird(230, 350)
        birds.append(bird)
        g.fitness = 0
        ge.append(g)

    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True
    paused = False

    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    if os.path.exists("checkpoint.pkl"):
                        os.remove("checkpoint.pkl")
                    pygame.quit()
                    quit()

        if paused:
            draw_window(win, birds, pipes, score, GEN, paused=True)
            continue

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1
            output = nets[i].activate((
                bird.y,
                abs(bird.y - pipes[pipe_ind].height),
                abs(bird.y - pipes[pipe_ind].bottom)
            ))
            if output[0] > 0.5:
                bird.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= WIN_HEIGHT or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        draw_window(win, birds, pipes, score, GEN)

    best = max([g.fitness for g in ge]) if ge else 0
    fitness_history.append(best)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    if os.path.exists("checkpoint.pkl"):
        with open("checkpoint.pkl", "rb") as f:
            population = pickle.load(f)
    else:
        population = neat.Population(config)

    while True:
        winner = population.run(main, 1)

        with open("checkpoint.pkl", "wb") as f:
            pickle.dump(population, f)

        with open("best_bird.pkl", "wb") as f:
            pickle.dump(winner, f)

        if len(fitness_history) > 1:
            plt.clf()
            plt.plot(fitness_history)
            plt.title("Best Fitness per Generation")
            plt.xlabel("Generation")
            plt.ylabel("Fitness")
            plt.grid(True)
            plt.pause(0.01)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    run(config_path)
