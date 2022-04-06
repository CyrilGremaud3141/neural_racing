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

population_size = 100
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
	car1 = deepcopy(cs[0])
	car2 = deepcopy(cs[1])

	cars.append(car1)
	cars.append(car2)
	for r in range(rand_cars):
		cars.append(CarAI(track))

	for i in range(population_size - 2 - rand_cars):
		c = deepcopy(car1)
		lay = random.randint(0, len(c.nn.net)-1)
		neu = random.randint(0, len(c.nn.net[lay])-1)
		# c.nn.net[lay][neu] = deepcopy(car2.nn.net[lay][neu])
		c.nn.net[lay][neu].randomize()
		
		cars.append(c)

	for c in cars:
		c.reset()
	return cars


cars = []
for i in range(population_size):
	cars.append(CarAI(track))

for gen in range(generations):
	print(gen)	
	for timesteps in tqdm(range(500 + (2 * gen))):
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
