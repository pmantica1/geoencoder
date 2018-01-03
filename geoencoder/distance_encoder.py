class DistanceEncoder():
	def __init__(self, base_lat=31, base_long=41):
		"""
		The default base location is in the middle of the Atlantic ocean  
		"""
		self.base_lat = base_lat
		self.base_long = base_long

	def encode(self, location):
		latitude = (location.bottom +location.top)/2
		if location.right >= location.left:
			longitude = (location.right+location.left)/2
		else:
			to_wrap_around = 180-location.left
			remaining_dist = location.right+180
			#Weighted average of location.left and location.right 
			longitude = ((to_wrap_around)*location.left+location.right*remaining_dist)/(to_wrap_around+remaining_dist)

		norm_latitude = (latitude-self.base_lat)
		norm_latitude = (norm_latitude if norm_latitude > -90 else norm_latitude+180)
		norm_longitude = (longitude-self.base_long)
		norm_longitude = (norm_longitude if norm_longitude > -180 else norm_longitude+360)
		return norm_latitude, norm_longitude




