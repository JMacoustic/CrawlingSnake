class TimeCounter:
	def __init__(self, t0):
		self.t = t0
	def update_time(self, dt):
		self.t += dt
	def print_time(self):
		print("current time: ", self.t)