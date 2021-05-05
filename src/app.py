import cv2
from polygon_drawer import PolygonDrawer
from tracker import Tracker
from distance_calculator import DistanceCalculator
from unit_converter import UnitConverter
from rect_matcher import RectMatcher
from tracker_drawer import TrackerDrawer
from csv_writer import CsvWriter
from center_finder import CenterFinder


window_name = 'pink_brain'
is_background = False


def run():
    # user input
    box_width = int(input('please enter the box width: '))
    box_height = int(input('please enter the box height: '))
    video_input_file_name = input('please enter the path to video file: ')
    video_output_file_name = f'{video_input_file_name}.output.avi'
    csv_output_file_name = f'{video_input_file_name}.output.csv'

    # setup video settings
    cap = cv2.VideoCapture(video_input_file_name)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # get first frame, must be the empty box
    first_frame = get_first_frame(cap)

    # setup areas
    center = CenterFinder.find_center(0.35, width, height)
    mid_x = int(width / 2)
    mid_y = int(height / 2)
    q1 = (0, 0), (mid_x, mid_y)
    q2 = (mid_x, 0), (width, mid_y)
    q3 = (0, mid_y), (mid_x, height)
    q4 = (mid_x, mid_y), (width, height)
    areas = {'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'center': center}

    # setup floor
    polygon_drawer = PolygonDrawer(window_name, first_frame, 4, 4)
    floor_points = polygon_drawer.draw()

    # track animal, convert unit measurement and calculate elapsed distance
    tracker = Tracker(cap, width, height, floor_points, first_frame)
    unit_converter = UnitConverter(width, height, box_width, box_height)
    distance_calculator = DistanceCalculator()
    rect_matcher = RectMatcher(areas)

    tracks = tracker.get_tracks()
    tracks = map(unit_converter.apply, tracks)
    tracks = map(distance_calculator.apply_distance, tracks)
    tracks = map(rect_matcher.apply_found_matches, tracks)

    # output the csv and the video
    csv_writer = CsvWriter(csv_output_file_name)
    tracker_drawer = TrackerDrawer(window_name, cap, video_output_file_name, is_background, areas)

    for track in tracks:
        csv_writer.append_line(track)
        tracker_drawer.draw(track)

    # release resources
    cap.release()
    cv2.destroyAllWindows()


def get_first_frame(cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    _, frame_without_animal = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    return frame_without_animal


if __name__ == "__main__":
    run()
