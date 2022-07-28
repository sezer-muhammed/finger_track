import cv2
import numpy as np
from angle_calculator import AngleCalculator
from color_detetor import ColorManager
from eklem_tracker import EklemTracker
import logging
from datetime import datetime
import json

now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
logging.basicConfig(filename=f"logs/{now}_HandTrackingRecord.txt", filemode="w", format="%(levelname)s | %(relativeCreated)d | %(module)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


cam_name = "manipulandum_red.mp4"
cam = cv2.VideoCapture(cam_name)

logger.info(f"Camera Started: {cam_name}")

for i in range(150):
    _, frame = cam.read()

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

hMin = 86
sMin = 74
vMin = 31
hMax = 163
sMax = 255
vMax = 255

logger.info(f"Filtering Values Set. Hue Min: {hMin}, Saturation Min: {sMin}, Value Min: {vMin}, Hue Max: {hMax}, Saturation Max: {sMax}, Value Max: {vMax}")

color_manager.update_color_range(hMin, sMin, vMin, hMax, sMax, vMax)

_, frame = cam.read()
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame_rgb = cv2.resize(frame_rgb, (1280, 720))
frame = joint_tracker.initialize_joints(frame_rgb, color_manager)
angle_calculator = AngleCalculator(logger)


logger.info(f"Starting Loop For video. \n\n\n")
while True:
    _, frame = cam.read()

    if _ == False:
        break

    frame = cv2.resize(frame, (1280, 720))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    empty = np.zeros((720, 1280, 3), np.uint8)
    logger.info(f"Frame read and resized to {frame.shape}.")

    color_manager.filter_points(frame_rgb)
    points = color_manager.get_points()
    joint_tracker.match(points)
    
    joint_tracker.draw(frame)

#    for p in points:
#        cv2.circle(frame, (int(p[0]), int(p[1])), 6, (255, 255, 255), -1, cv2.LINE_AA)

    joints = joint_tracker.get_joints()
    angles = angle_calculator.get_angle(joints)

    joint_list = list(joints.keys())
    logger.info(f"Angles & Lines Are on the Image")
    for i, j in enumerate(joints):
        try:
            cv2.line(frame, (int(joints[j][0]), int(joints[j][1])), (int(joints[joint_list[i+1]][0]), int(joints[joint_list[i+1]][1])), (0, 255, 0), 2, cv2.LINE_AA)
            cv2.line(empty, (int(joints[j][0]), int(joints[j][1])), (int(joints[joint_list[i+1]][0]), int(joints[joint_list[i+1]][1])), (0, 255, 0), 2, cv2.LINE_AA)
        except:
            pass

    for i, angle in enumerate(angles):
        cv2.putText(frame, f"{round(angles[angle], 1)}", (int(joints[angle][0]), int(joints[angle][1]) - 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (2, 10, 255), 1, cv2.LINE_AA)
        # TODO ADD ARC
        p1 = joints[joint_list[i+1+1]]
        p2 = joints[angle]
        p3 = joints[joint_list[i+1-1]]

        world_angle = np.arctan( (p2[1] - p1[1]) / (p2[0] - p1[0]) ) * 180 / np.pi

        if i > 2:
            cv2.ellipse(frame, (int(p2[0]), int(p2[1])), (20, 20), world_angle - 180, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)
            cv2.ellipse(empty, (int(p2[0]), int(p2[1])), (20, 20), world_angle - 180, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)
        else:
            cv2.ellipse(frame, (int(p2[0]), int(p2[1])), (20, 20), world_angle, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)
            cv2.ellipse(empty, (int(p2[0]), int(p2[1])), (20, 20), world_angle, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)

    cv2.imshow("Image", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    video_writer.write(frame)
    empty_writer.write(empty)
    logger.info(f"Frame Saved.\n\n\n\n\n")

logger.info(f"All Joint Positions: {joint_tracker.get_all()}\n\n\n\n")
logger.info(f"All Joint Angles: {angle_calculator.get_all()}")
video_writer.release()
empty_writer.release()