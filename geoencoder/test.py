import unittest
from grid_encoder import GridEncoder
from location import Location
from distance_encoder import DistanceEncoder
from overlapping_grid_encoder import OverlappingGridEncoder

class TestGridEncoder(unittest.TestCase): 
    def test_encode_decode_simple(self):
        loc = Location(5, 5, 5, 5) 
        grid_encoder = GridEncoder(r                                                        esolution=5)
        encoded_loc = grid_encoder.encode(loc)
        decoded_loc = grid_encoder.decode(encoded_loc)
        self.assertEqual(loc, decoded_loc)

    def test_encode_decode_non_integer(self):
        loc = Location(-2, 3.3, -3, 5.5)
        grid_encoder = GridEncoder(resolution=5)
        encoded_loc = grid_encoder.encode(loc)
        decoded_loc = grid_encoder.decode(encoded_loc)
        self.assertEqual(Location(-5, 0, -5, 5), decoded_loc)

    def test_encoder_decode_wrap_around(self):
        loc = Location(0, 80, 170, -170)
        grid_encoder = GridEncoder(resolution=10)
        encoded_loc = grid_encoder.encode(loc)
        decoded_loc = grid_encoder.decode(encoded_loc)
        self.assertEqual(loc, decoded_loc)

    def test_encoder_decode_wrap_around_non_integer(self):
        loc = Location(15.5, 85.5, 171.1, -172.3)
        grid_encoder = GridEncoder(resolution=5)
        encoded_loc = grid_encoder.encode(loc)
        decoded_loc = grid_encoder.decode(encoded_loc)
        self.assertEqual(Location(15, 85, 170, -175), decoded_loc)

    def test_overlapping_grid_encoder(self):
        loc = Location(5, 5, 5, 5) 
        grid_encoder = OverlappingGridEncoder(resolutions=[10, 5])
        encoded_loc = grid_encoder.encode(loc)
        decoded_loc = grid_encoder.decode(encoded_loc)
        self.assertEqual(loc, decoded_loc)

    def test_distance_encoder_normal(self):
        loc = Location(5, 11, 6, 32)
        distance_encoder = DistanceEncoder()
        encoded_loc = distance_encoder.encode(loc)
        self.assertEqual((-23, -22), encoded_loc)

    def test_distance_encoder_overflow(self):
        loc = Location(-90, -90, -180, -180)
        distance_encoder = DistanceEncoder()
        encoded_loc = distance_encoder.encode(loc)
        self.assertEqual((59, 139), encoded_loc)

    def test_distance_encoder_wrap_around(self):
        loc = Location(31, 31, 170, -160)
        distance_encoder = DistanceEncoder()
        encoded_loc = distance_encoder.encode(loc)
        self.assertEqual((0, -91), encoded_loc)

if __name__ == "__main__":
    unittest.main()