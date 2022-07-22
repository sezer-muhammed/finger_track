import cv2
import numpy as np
from angle_calculator import AngleCalculator
from color_detetor import ColorManager
from eklem_tracker import EklemTracker

cam = cv2.VideoCapture("mavi-el.mp4")
cv2.namedWindow("Image")

fps = cam.get(cv2.CAP_PROP_FPS)
w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

video_writer = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (1280, 720))

kernel = np.ones((5,5),np.uint8)

color_manager = ColorManager()
joint_tracker = EklemTracker()

hMin = 95
sMin = 69
vMin = 38
hMax = 170
sMax = 232
vMax = 255

color_manager.update_color_range(hMin, sMin, vMin, hMax, sMax, vMax)

_, frame = cam.read()
frame = joint_tracker.initialize_joints(frame, color_manager)
angle_calculator = AngleCalculator()


while True:
    _, frame = cam.read()

    if _ == False:
        break

    frame = cv2.resize(frame, (1280, 720))

    color_manager.filter_points(frame)
    points = color_manager.get_points()
    joint_tracker.match(points)
    
    joint_tracker.draw(frame)

#    for p in points:
#        cv2.circle(frame, (int(p[0]), int(p[1])), 6, (255, 255, 255), -1, cv2.LINE_AA)

    joints = joint_tracker.get_joints()
    angles = angle_calculator.get_angle(joints)

    joint_list = list(joints.keys())
    for i, j in enumerate(joints):
        try:
            cv2.line(frame, (int(joints[j][0]), int(joints[j][1])), (int(joints[joint_list[i+1]][0]), int(joints[joint_list[i+1]][1])), (0, 255, 0), 4, cv2.LINE_AA)
        except:
            pass

    for angle in angles:
        cv2.putText(frame, f"{round(angles[angle], 1)}", (int(joints[angle][0]), int(joints[angle][1]) - 50), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 150, 255), 2, cv2.LINE_AA)


    cv2.imshow("Image", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    video_writer.write(frame)

print(joint_tracker.get_all())
print(angle_calculator.get_all())

video_writer.release()