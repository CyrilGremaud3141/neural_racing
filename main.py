from Track import *
from Car import *
from CarAI import *
from Monaco import setupMonaco
from Traces import clearTraces, saveTraces
from render import Render
from tqdm import tqdm
from multiprocessing import Process, Manager
import random
from copy import deepcopy
from ShowNet import NetRender
import os



generations = 10000
batch_size = 25
rand_cars = 10
max_time_steps = 3000

num_processes = 24

population_size = num_processes * batch_size

track = setupMonaco()




def step(car, ren=False):
	if car.gameOver:
		pass
	else:
		car.control()
		car.move()
		car.updateScore()
		if car.checkCollision() or car.score > 2000:
			car.gameOver = True
	if ren:
		render.renderCar(int(car.x), int(car.y), int(car.rot))

def render_net(car):
	net = car.nn
	netrender.drawNet(net)
	netrender.show()

render = Render(track, 1000, 500)
netrender = NetRender(1000, 500)

def newCars(cs):
	# random.shuffle(cs)
	render_net(cs[0])
	cars = []
	best_cars = cs[:5]
	for b in best_cars:
		b.reset()
	for i in range(population_size - rand_cars):
		cars.append(deepcopy(best_cars[i % 5]))

	for i in range(rand_cars):
		cars.append(CarAI(track))
	
	for car in cars[5:]:
		car.nn.mutate()
	
	return cars


def train_batch(batch, process_idx, return_dict, gen):
	for timesteps in range(min(max_time_steps, 500 + (300 * gen))):
		for car in batch:
			step(car)

	return_dict[process_idx] = batch

def train_visualized_batch(batch):
	for timesteps in tqdm(range(min(max_time_steps, 500 + (300 * gen)))):
		render.render()
		for car in batch:
			step(car, ren=True)
		render.show()


if __name__ == '__main__':
	cars = []
	name = 'moin'
	for i in range(population_size):
		cars.append(CarAI(track))

	if os.path.isfile(name + '.txt'):
		cars[0].nn.load(name)
	render_net(cars[0])

	for gen in range(generations):
		batches = []
		batch = []
		for car in cars:
			batch.append(car)
			if len(batch) == batch_size:
				batches.append(batch)
				batch = []


		processes = []
		return_dict = Manager().dict()
		for i, batch in enumerate(batches[1:]):
			p = Process(target=train_batch, args=[batch, i, return_dict, gen])
			p.start()
			processes.append(p)

		train_visualized_batch(batches[0])

		for p in processes:
			p.join()
		cars = batches[0]
		for b in return_dict.values():
			cars += b


		cars.sort(key=lambda car: car.score, reverse=True)
		cars[0].nn.save("moin")

		print(f'Generation: {gen}, best score: {cars[0].score}')

		cars = newCars(cars)


	# # clearTraces()

	# # saveTraces(cars)

	for car in cars:
		print(car.score, car.x, car.y, car.getLifetime())
