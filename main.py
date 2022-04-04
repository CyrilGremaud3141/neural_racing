from Track import *
from Car import *
from CarAI import *
from Monaco import setupMonaco
from Traces import clearTraces, saveTraces
from render import Render
from tqdm import tqdm


# Race between two random cars
# Replace dummy network with your network later

population_size = 100
generations = 1


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
	render.renderCar(int(car.x), int(car.y))

render = Render(track, 1000, 500)




for gen in range(generations):
	cars = []
	for i in range(population_size):
		cars.append(CarAI(track))
	print(gen)	
	for timesteps in tqdm(range(1000)):
		render.render()
		for car in cars:
			step(car)
		render.show()
	cars.sort(key=lambda car: car.score, reverse=True)

# clearTraces()

# saveTraces(cars)

for car in cars:
	print(car.score, car.x, car.y, car.getLifetime())
