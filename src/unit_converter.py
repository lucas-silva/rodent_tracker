import numpy as np


class UnitConverter:
    def __init__(self, source_width, source_height, destination_width, destination_height):
        self.coefficient = destination_width / source_width, destination_height / source_height
        self.area_coefficient = (destination_width * destination_height) / (source_width * source_height)

    def apply(self, track):
        if track['animal']:
            track['animal']['xy_physical'] = tuple(np.multiply(track['animal']['xy'], self.coefficient))
            track['animal']['contour_area_physical'] = track['animal']['contour_area'] * self.area_coefficient

        return track
