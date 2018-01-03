class Location():
    def __init__(self, bottom, top, left, right):
        # Range for latitude is [-90, 90 ) and [-180, 180 )
        assert top >= bottom, "Expected no latitude wrap around (top<bottom)"
        assert 90 >= bottom >= -90, "Bottom out of range"
        assert 90 >= top >= -90, "Top out of range"
        assert 180 >= left >= -180, "Left out of range"
        assert 180 >= right >= -180, "Right out of range"
        self.bottom = bottom;
        self.left = left;
        self.top = top;
        self.right = right;

    def __eq__(self, other):
        matching_lat_boxes = self.bottom == other.bottom and self.top == other.top
        matching_long_boxes = self.left == other.left and self.right == other.right
        return matching_long_boxes and matching_lat_boxes

    def __str__(self):
        return "bottom: %s | top: | %s | left: %s | right: %s" % (self.bottom, self.top, self.left, self.right)
