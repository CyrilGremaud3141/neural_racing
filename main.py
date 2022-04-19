from hashlib import new

from cv2 import cartToPolar
from sklearn.ensemble import RandomTreesEmbedding
from Track import *
from Car import *
from CarAI import *
from Monaco import setupMonaco
from Traces import clearTraces, saveTraces
from render import Render
from tqdm import tqdm
from multiprocessing import Process
import random
from copy import deepcopy



# Race between two random cars
# Replace dummy network with your network later

population_size = 50
generations = 10000

rand_cars = 10


track = setupMonaco()




def step(car):
	if car.gameOver:
		pass
	else:
		car.control()
		car.move()
		car.updateScore()
		if car.checkCollision() or car.score > 2000:
			car.gameOver = True
	render.renderCar(int(car.x), int(car.y), car.score)

render = Render(track, 1000, 500)


def newCars(cs):
	cars = []
	best_car = cs[0]
	best_car.reset()
	for i in range(population_size):
		cars.append(deepcopy(best_car))
	
	for car in cars[1:]:
		car.nn.mutate()
	
	return cars


cars = []
for i in range(population_size):
	cars.append(CarAI(track))

for gen in range(generations):
	print(gen)	
	for timesteps in tqdm(range(500 + (50 * gen))):
		render.render()
		for car in cars:
			step(car)
		render.show()
	cars.sort(key=lambda car: car.score, reverse=True)

	cars = newCars(cars)

# clearTraces()

# saveTraces(cars)

for car in cars:
	print(car.score, car.x, car.y, car.getLifetime())
