import pygame
import time
import random
from math import inf

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_between(self, node):
        return ((self.x - node.x) ** 2 + (self.y - node.y) ** 2) ** 0.5

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.distance = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5



gameover= False

height = 400
width = 600

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame!")
clock = pygame.time.Clock()


def generate_random_path(citys):
    path = []
    for i in range(len(citys)):
        path.append(i)
    random.shuffle(path)
    return path

def path_distance(path, citys):
    distance = 0
    for i in range(len(path)):
        if i == len(path) - 1:
            distance += citys[path[i]].distance_between(citys[path[0]])
        else:
            distance += citys[path[i]].distance_between(citys[path[i + 1]])
    return distance

def mutate(population, mutation_rate):
    # print("len pop", len(population))
    mutations = int(len(population)*mutation_rate)
    cromosome_mutations = 1
    # print("mutations", mutations)
    new_population = []
    for i in range(len(population)):

        r = random.random()
        if r < mutation_rate:
            for _ in range(cromosome_mutations):
                a = random.randint(0, len(population[i]) - 1)
                b = random.randint(0, len(population[i]) - 1)
                # mt = pick_one(population, citys)
                mt = population[i]
                mt[a], mt[b] = mt[b], mt[a]
                new_population.append(mt)
        else:
            new_population.append(population[i])

    return new_population

def genetic_salesman(citys, population_size, mutation_rate, screen):
    population = [generate_random_path(citys) for _ in range(population_size)]
    best_path_ever = population[0]
    itr = 0
    while itr < 1000:
        itr += 1
        population = sorted(population, key=lambda x: path_distance(x, citys))
        
        if path_distance(population[0], citys) < path_distance(best_path_ever, citys):
            best_path_ever = population[0].copy()
        
        draw_path(population[0], citys, screen)

        population = mutate(population, mutation_rate)
    print(best_path_ever)
    return best_path_ever

def pick_one(population, citys):
    r = random.randint(0, 5)
    return population[r]


citys = []
# for _ in range(10):
#     citys.append(Node(random.randint(0, width), random.randint(0, height)))

def draw_path(path, citys, screen):
    screen.fill(black)
    for i in range(len(citys)):
        pygame.draw.circle(screen, green, (citys[i].x, citys[i].y), 5)

    if path == []:
        return
    for i in range(len(path)):
        if i == len(path) - 1:
            pygame.draw.line(screen, blue, (citys[path[i]].x, citys[path[i]].y), (citys[path[0]].x, citys[path[0]].y), 1)
        else:
            pygame.draw.line(screen, blue, (citys[path[i]].x, citys[path[i]].y), (citys[path[i + 1]].x, citys[path[i + 1]].y), 1)
    pygame.display.update()
    # time.sleep(0.1)


best_path = []
while not gameover:

    for event in pygame.event.get():
        screen.fill(black)

        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                best_path = genetic_salesman(citys, 100, 0.1, screen)
                print("best path", best_path, "distance", path_distance(best_path, citys))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.draw.circle(screen, red, event.pos, 10)
                n = Node(event.pos[0], event.pos[1])
                print("City Added")
                citys.append(n)
            if event.button == 3:
                mx, my = pygame.mouse.get_pos()
                for i in range(len(citys)):
                    if citys[i].x - 10 < mx < citys[i].x + 10 and citys[i].y - 10 < my < citys[i].y + 10:
                        citys.pop(i)
                        break
                print("Nearrest city removed")
                


        for i in range(len(citys)):
            pygame.draw.circle(screen, green, (citys[i].x, citys[i].y), 5)

        draw_path(best_path, citys, screen)
        pygame.display.update()

    clock.tick_busy_loop(60)

pygame.quit()

