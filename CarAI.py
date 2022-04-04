from Car import Car
from ai import NeuralNet

class CarAI(Car):

	def __init__(self, track):
		super().__init__(track)
		self.nn = NeuralNet(6, [4, 5], 2)


	def control(self):
		scans = self.getScans()
		results = self.nn.forward([*scans, self.v])
		self.acc = -1 + 2 * results[0]
		self.steer = -1 + 2 * results[1]
