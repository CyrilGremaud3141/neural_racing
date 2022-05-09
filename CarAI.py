from Car import Car
from neat import NeuralNet

class CarAI(Car):

	def __init__(self, track):
		super().__init__(track)
		self.nn = NeuralNet(6, 2)


	def control(self):
		scans = self.getScans()
		results = self.nn.forward([*scans, self.v])
		self.acc = -1 + 2 * results[0]
		self.acc = 1
		self.steer = -1 + 2 * results[1]

		self.acc = min(self.acc, 10)
