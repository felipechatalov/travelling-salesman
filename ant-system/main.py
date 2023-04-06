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

class Ant:
    def __init__(self, phPower, dstPower, evapRate, lookUpPh):
        self.phPower = phPower
        self.dstPower = dstPower # or 1 - phPower
        self.evapRate = evapRate
        self.lookUpPh = lookUpPh
        self.path = []
        self.initCity = random.randint(0, len(citys) - 1)
        self.distance = 0

    def solve(self, citys):
        self.path = [self.initCity]
        while len(self.path) < len(citys):
            self.path.append(self.pick_next_city(self.path[-1], citys))
        self.distance = path_distance(self.path, citys)
        return self.path, self.distance


    def pick_next_city(self, current_city, citys):
        probabilities = []
        for i in range(len(citys)):
            if i not in self.path:
                probabilities.append(
                    (self.lookUpPh[current_city][i] ** self.phPower) * (1 / citys[current_city].distance_between(citys[i]) ** self.dstPower))
            else:
                probabilities.append(0)
        probabilities = [x / sum(probabilities) for x in probabilities]
        r = random.random()
        for i in range(len(probabilities)):
            if r < probabilities[i]:
                return i
            else:
                r -= probabilities[i]


class Colony:
    def __init__(self, citys, pheromonePower, distancePower, pheromoneIntensity, initPheromoneIntensity, evaporationRate, colonySize):
        self.citys = citys
        self.pheromonePower = pheromonePower
        self.distancePower = distancePower
        self.pheromoneIntensity = pheromoneIntensity
        self.initPheromoneIntensity = initPheromoneIntensity
        self.evaporationRate = evaporationRate
        self.colonySize = colonySize
        self.ants = []
        self.lookUpPheromone = [[initPheromoneIntensity for _ in range(len(citys))] for _ in range(len(citys))]

    def generate_ants(self):
        for _ in range(self.colonySize):
            self.ants.append(Ant( 
                                 self.pheromonePower, 
                                 self.distancePower, 
                                 self.evaporationRate, 
                                 self.lookUpPheromone))

    def update_pheromone(self):
        for i in range(len(self.lookUpPheromone)):
            for j in range(len(self.lookUpPheromone)):
                self.lookUpPheromone[i][j] *= self.evaporationRate
                if i == j:
                    self.lookUpPheromone[i][j] = 0
        for ant in self.ants:
            for i in range(len(ant.path)):
                if i == len(ant.path) - 1:
                    self.lookUpPheromone[ant.path[i]][ant.path[0]] += 1 / ant.distance
                else:
                    self.lookUpPheromone[ant.path[i]][ant.path[i + 1]] += 1 / ant.distance

    def regenerate_pheromone(self):
        for i in range(len(self.lookUpPheromone)):
            for j in range(len(self.lookUpPheromone)):
                self.lookUpPheromone[i][j] = self.initPheromoneIntensity

    def solve(self):
        self.generate_ants()
        results = []
        for _ in range(2):
            for ant in self.ants:
                s = ant.solve(citys)
                # print(s)
                results.append(s)
            self.update_pheromone()

        return results

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


def path_distance(path, citys):
    distance = 0
    for i in range(len(path)):
        if i == len(path) - 1:
            distance += citys[path[i]].distance_between(citys[path[0]])
        else:
            distance += citys[path[i]].distance_between(citys[path[i + 1]])
    return distance

citys = []
def draw_citys(citys, screen):
    screen.fill(black)
    for i in range(len(citys)):
        pygame.draw.circle(screen, (255, 255 - i * 255 / (len(citys)+1), 0), (citys[i].x, citys[i].y), 5)

def draw_path(path, citys, screen, sleep_time):
    if path == []:
        return
    for i in range(len(path)):
        if i == len(path) - 1:
            pygame.draw.line(screen, blue, (citys[path[i]].x, citys[path[i]].y), (citys[path[0]].x, citys[path[0]].y), 1)
        else:
            pygame.draw.line(screen, blue, (citys[path[i]].x, citys[path[i]].y), (citys[path[i + 1]].x, citys[path[i + 1]].y), 1)
    pygame.display.update()
    time.sleep(sleep_time)

best_path = []
# parametros podem ser modificados, aumentando o numero de caminhos aleatorios, diminuindo evaporacao do feromonio
# ou fazendo o algoritmo funcionar mais como um algoritmo guloso
colony = Colony(citys, 1, 4, 10, 1, -0.3, 100)
while not gameover:

    for event in pygame.event.get():
        screen.fill(black)

        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                print("[Debug] Showing variables:")
                print("citys", [(city.x, city.y) for city in citys])
                print("best_path", best_path)
                print("'best_path' path distance", path_distance(best_path, citys))
                print("colony", colony)
                print("colony.citys", colony.citys)
                print("colony.pheromonePower", colony.pheromonePower)
                print("colony.distancePower", colony.distancePower)
                print("colony.pheromoneIntensity", colony.pheromoneIntensity)
                print("colony.initPheromoneIntensity", colony.initPheromoneIntensity)
                print("colony.evaporationRate", colony.evaporationRate)
                print("colony.colonySize", colony.colonySize)
                print("colony.ants", colony.ants)
                print("colony.lookUpPheromone", colony.lookUpPheromone)
                print("colony.ants[0]", colony.ants[0])
                print("colony.ants[0].path", colony.ants[0].path)
                print("colony.ants[0].distance", colony.ants[0].distance)
                print("colony.ants[0].citys", colony.ants[0].citys)

            if event.key == pygame.K_a:
                now = time.perf_counter()
                
                # colony.citys = citys
                # colony.regenerate_pheromone()
                colony = Colony(citys, 1, 4, 10, 1, -0.3, 5)
                r_collection = []
                best_path = [i for i in range(len(citys))]
                for i in range(1):
                    path_and_distances = colony.solve()
                    r_collection.append(path_and_distances)
                    print(len(path_and_distances))
                    for j in range(len(path_and_distances)):
                        if path_distance(path_and_distances[i][0], citys) < path_distance(best_path, citys):
                            best_path = path_and_distances[i][0]


                print("Results:")
                for i in range(len(r_collection)):
                    print("Path:", r_collection[i][0][0], "Distance", path_distance(r_collection[i][0][0], citys))
                print("Best path", best_path, "Distance", path_distance(best_path, citys), ", Time", time.perf_counter() - now)           

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.draw.circle(screen, red, event.pos, 50)
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
                

        draw_citys(citys, screen)
        draw_path(best_path, citys, screen, 0)

        pygame.display.update()

    clock.tick_busy_loop(60)

pygame.quit()

