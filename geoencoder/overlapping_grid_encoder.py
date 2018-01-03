import numpy as np 
from grid_encoder import GridEncoder

class OverlappingGridEncoder():
	def __init__(self, resolutions):
		self.grid_encoders = [GridEncoder(res) for res in sorted(resolutions)]

	def encode(self, location):
		encodings = [] 
		for grid_encoder in self.grid_encoders:
			encodings.append(np.ndarray.flatten(grid_encoder.encode(location)))
		return np.concatenate(encodings)

	def decode(self, encoding):
		prime_grid_encoder = self.grid_encoders[0]
		flattened_grid = encoding[:prime_grid_encoder.num_points]
		grid = flattened_grid.reshape(prime_grid_encoder.latitude_enc_length, prime_grid_encoder.longitude_enc_length)
		return prime_grid_encoder.decode(grid)


