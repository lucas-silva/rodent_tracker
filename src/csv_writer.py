import math


class CsvWriter:
    previous_ms = None

    def __init__(self, file_name):
        self.file = open(file_name, 'w')
        self.file.write('frame_number,x,y,distance,ms,elapsed_time,area,quarter,animal_area\n')

    def append_line(self, track):
        if track['animal']:
            frame_number = track['frame_number']
            x, y = track['animal']['xy_physical']
            distance = track['distance']
            ms = track['frame_ms']
            ms_elapsed_in_day_scale = track['frame_elapsed_ms'] / 1000 / 86400
            area = track['animal']['area']
            quarter = track['animal']['quarter']
            animal_area = math.sqrt(track['animal']['contour_area_physical'])

            self.file.write(
                f'{frame_number},{x},{y},{distance},{ms},{ms_elapsed_in_day_scale},{area},{quarter},{animal_area}\n'
            )

    def __exit__(self):
        self.file.close()
