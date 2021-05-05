class RectMatcher:
    def __init__(self, areas):
        self.areas = areas

    def apply_found_matches(self, track):
        if track['animal']:
            x, y = track['animal']['xy']

            track['animal']['area'] = 'internal'
            track['animal']['quarter'] = ''

            for key in self.areas:
                area = self.areas[key]
                top_left, bottom_right = area
                min_x, min_y = top_left
                max_x, max_y = bottom_right
                is_match = min_x < x < max_x and min_y < y < max_y

                if is_match:
                    if key in ('q1', 'q2', 'q3', 'q4'):
                        track['animal']['quarter'] = key
                    elif key == 'center':
                        track['animal']['area'] = 'center'

        return track
