import math
import numpy as np


class DistanceCalculator:
    previous_xy = None

    def apply_distance(self, track):
        xy = track['animal']['xy_physical'] if track['animal'] else None
        distance = math.hypot(*np.subtract(self.previous_xy, xy)) if xy and self.previous_xy else 0

        self.previous_xy = xy

        return {
            **track,
            'distance': distance
        }
