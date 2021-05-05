# Rodent Tracker
## Introduction
Software to track rodents

## Requirements
- Windows or Linux based operational system
- ffmpeg or K-Lite Codec Pack
- python >= 3.8 
- pipenv

## Running instructions
### Windows
run on your terminal
```
.\Scripts\activate
pipenv install
python src/main.py
```
### Linux
run on your terminal
```
pipenv shell
pipenv install
python src/main.py
```

## Limitations
- The first frame must be an empty box, because we subtract it from next frames to isolate the animal 
- The floor area must be drawn in clockwise direction
- The output video fast-forward
- We are not able to identify the external area

## Usage
- Enter the box dimensions (width and height in cm or other unit system)
- Enter the path to the video
- Define floor area (**NOTE:** draw points in clockwise direction)

## Output
- ### output video file
    - The video with the contours interpreted by the program, useful to validate if the tracking is fine

         https://user-images.githubusercontent.com/6013524/118596957-71559e00-b782-11eb-8c64-83b9040f8b81.mp4

- ### csv file
    | frame_number | x | y | distance | ms | time_elapsed | area | quarter | animal_area |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 53 | 121 | 344 | 0 | 100 | 00:00:06,10 | internal | q1 | 7.06 |
    | 54 | 147 | 305 | 47 | 133 | 00:00:06,23 | internal | q2 | 12.85 |
    | 55 | 133 | 283 | 26 | 137 | 00:00:06,33 | center | q3 | 16.43 |
    | 57 | 175 | 284 | 18 | 167 | 00:00:06,57 | center | q1 | 14.98 |
    | 58 | 183 | 281 | 9 | 180 | 00:00:06,70 | center | q2 | 7.60 |
  
   - **Columns**
        - frame_number: the number of video frame 
        - x: the x position of animal 
        - y: the y position of animal
        - distance: the distance from previous frame
        - ms: the milliseconds from previous frame 
        - time_elapsed: the time elapsed in day scale, format as time **[HH]:MM:SS,00** on spreadsheet
        - area: the area which the animal were *(center, internal)*
            - center: is a rectangle in the center (the size is settable, default value is box's 35% size)
            - internal: is the floor, except the center
        - quarter: the quarter which the animal were
            - there are four quarters, the position of each is represented below:
        
                | Left Side of Video | Right Side of Video |
                | :---: | :---: |
                | q1 | q2 |
                | q3 | q4 |
       - animal_area: the square area of animal
    - **Kinds of data you can extract**
        - [x] Total distance by summing distance column
        - [x] Total spent time by summing time column
        - [x] Area distance by filtering by area and summing distance column
        - [x] Area spent time by filtering by area column and summing time column
        - [x] Quarter distance by filtering by quarter and summing distance column
        - [x] Quarter spent time by filtering by quarter column and summing time column
        - [x] View where animal were by filtering x y columns close to your target object helping to find interactions 

## Thanks for colinlaney's who inspired this code
- https://github.com/colinlaney/animal-tracking

## Related projects
- https://github.com/DeepLabCut/DeepLabCut
- https://github.com/Ferill/OpenBarnes
- https://github.com/Haptein/OFTrack
- https://github.com/Keats/rodent
- https://github.com/SainsburyWellcomeCentre/Pyper
- https://github.com/TheChymera/behaviopy
- https://github.com/omaghsoudi/3D-Paw-Tracking-Edition-Python
- https://github.com/pspratt/MouseTracker
- https://github.com/sraorao/animapp_conda

## Related papers
- https://towardsdatascience.com/detecting-animals-in-the-backyard-practical-application-of-deep-learning-c030d3263ba8
