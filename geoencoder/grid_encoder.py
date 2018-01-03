import numpy as np
import math


class GridEncoder():
    def __init__(self, resolution=5):
        self.resolution = resolution
        self.latitude_enc_length = int(math.ceil(180 / resolution))
        self.longitude_enc_length = int(math.ceil(360 / resolution))
        self.num_points = self.latitude_enc_length * self.longitude_enc_length

    def encode(self, location):
        grid = np.zeros((self.latitude_enc_length, self.longitude_enc_length))

        bottom_enc = int(math.floor((location.bottom + 90) / self.resolution))
        top_enc = int(math.floor((location.top + 90) / self.resolution))
        left_enc = int(math.floor((location.left + 180) / self.resolution))
        right_enc = int(math.floor((location.right + 180) / self.resolution))

        # Code to deal with edge cases (latitude = 180, latitude=90)
        bottom_enc = min(bottom_enc, self.latitude_enc_length-1)
        top_enc= min(top_enc, self.latitude_enc_length - 1)
        left_enc = min(left_enc, self.longitude_enc_length- 1)
        right_enc = min(right_enc, self.longitude_enc_length - 1)

        latitude_dif = (top_enc - bottom_enc + 1)

        if location.left <= location.right:
            longitude_dif = (right_enc - left_enc + 1)
            area = longitude_dif * latitude_dif
            inv_area = 1 / area
            mask = np.zeros((latitude_dif, longitude_dif))
            mask.fill(inv_area)
            grid[bottom_enc:top_enc + 1, left_enc:right_enc + 1] = mask
        else:
            longitude_to_wrap_around = (self.longitude_enc_length - left_enc)
            longtitude_left = (right_enc + 1)
            area = (longitude_to_wrap_around + longtitude_left) * latitude_dif
            inv_area = 1 / area
            mask_1 = np.zeros((latitude_dif, longitude_to_wrap_around))
            mask_1.fill(inv_area)
            maks_2 = np.zeros((latitude_dif, longtitude_left))
            maks_2.fill(inv_area)
            grid[bottom_enc:top_enc + 1, left_enc:self.longitude_enc_length] = mask_1
            grid[bottom_enc:top_enc + 1, :right_enc + 1] = maks_2

        assert abs(np.sum(np.sum(grid)) - 1) < 0.01
        return grid

    def decode(self, grid):
        exists_val_in_rows = [row_val > 0 for row_val in np.sum(grid, axis=1)]
        bottom = exists_val_in_rows.index(True) * self.resolution
        exists_val_in_rows.reverse()
        top = (len(exists_val_in_rows) - 1 - exists_val_in_rows.index(True)) * self.resolution

        exists_val_in_cols = [col_val > 0 for col_val in np.sum(grid, axis=0)]
        if not self.check_if_wrap_around(exists_val_in_cols):
            left = exists_val_in_cols.index(True) * self.resolution
            exists_val_in_cols.reverse()
            right = (len(exists_val_in_cols) - 1 - exists_val_in_cols.index(True)) * self.resolution
        else:
            right = (exists_val_in_cols.index(False) - 1) * self.resolution
            exists_val_in_cols.reverse()
            left = (len(exists_val_in_cols) - exists_val_in_cols.index(False)) * self.resolution

        return location.Location(bottom - 90, top - 90, left - 180, right - 180)

    def check_if_wrap_around(self, exists_val_in_cols):
        has_seen_start = False
        has_seen_end = False
        for exists_val_in_col in exists_val_in_cols:
            if has_seen_end:
                if exists_val_in_col:
                    return True
            elif has_seen_start:
                if not exists_val_in_col:
                    has_seen_end = True
            else:
                if exists_val_in_col:
                    has_seen_start = True
        return False

    def draw_encoding(self, encoding):
        import matplotlib.pyplot as plt
        plt.pcolormesh(encoding)
        plt.show()


if __name__ == "__main__":
    loc = location.Location(-90, 90, 180, -180)
    grid_encoder = GridEncoder(resolution=5)
    encoded_loc = grid_encoder.encode(loc)
    grid_encoder.draw_encoding(encoded_loc)
