import cv2
from imageio import save
import numpy as np
from angle_calculator import AngleCalculator
from color_detetor import ColorManager
from eklem_tracker import EklemTracker
import logging
from datetime import datetime
import json
import pandas as pd

now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
logging.basicConfig(filename=f"logs/{now}_HandTrackingRecord.txt", filemode="w", format="%(levelname)s | %(relativeCreated)d | %(module)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


cam_name = "yesil-el.mp4"
cam = cv2.VideoCapture(cam_name)

logger.info(f"Camera Started: {cam_name}")

cv2.namedWindow("Image")

fps = cam.get(cv2.CAP_PROP_FPS)
w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

output_name = "manipulandum_red_output.mp4"
video_writer = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (1280, 720))
empty_writer = cv2.VideoWriter("only-lines-" + output_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (1280, 720))

logger.info(f"Resolution H: {h}, W: {w}. Writer Object Created with the Name: {output_name}.")

kernel = np.ones((5,5),np.uint8)

color_manager = ColorManager(logger)
joint_tracker = EklemTracker(logger)

hMin = 24
sMin = 80
vMin = 20
hMax = 118
sMax = 255
vMax = 205

logger.info(f"Filtering Values Set. Hue Min: {hMin}, Saturation Min: {sMin}, Value Min: {vMin}, Hue Max: {hMax}, Saturation Max: {sMax}, Value Max: {vMax}")

color_manager.update_color_range(hMin, sMin, vMin, hMax, sMax, vMax)

while True:
    _, frame = cam.read()
    frame = cv2.resize(frame, (1280, 720))
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) == ord("q"):
        break

_, frame = cam.read()
frame = cv2.resize(frame, (1280, 720))
frame = joint_tracker.initialize_joints(frame, color_manager)
angle_calculator = AngleCalculator(logger)

logger.info(f"Starting Loop For video. \n\n\n")
while True:
    _, frame = cam.read()

    if _ == False:
        break

    frame = cv2.resize(frame, (1280, 720))
    empty = np.zeros((720, 1280, 3), np.uint8)
    logger.info(f"Frame read and resized to {frame.shape}.")

    color_manager.filter_points(frame)
    points = color_manager.get_points()
    joint_tracker.match(points)

    joints = joint_tracker.get_joints()
    angles = angle_calculator.get_angle(joints)

    #frame, empty = joint_tracker.draw(frame, empty, angles)
    
    joint_list = list(joints.keys())

    cv2.imshow("Image", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    video_writer.write(frame)
    empty_writer.write(empty)
    logger.info(f"Frame Saved.\n\n\n\n\n")

angle_data = pd.DataFrame(angle_calculator.get_all())
angle_data = angle_data.add_suffix('_angle')

angle_data.to_excel("joint_data.xlsx")

video_writer.release()
empty_writer.release()