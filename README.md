
# Finger Keypoint Tracker with OpenCV

This repo detects and tracks joints on finger that labeled some color.


## Class Reference

#### Angle Calculator

| Parameter | Input Object     | Description                |
| :-------- | :------- | :------------------------- |
| `__init__()` | `logging.getLogger()` | Your logging object. |
| `get_angle()` | `eklem_tracker.get_joints()` | Joints' dictionary, return angle of joints as dictionary|
| `get_all()` | | Returns all angle dictionaries as a list |

#### Color Detector

| Parameter | Input Object     | Description                |
| :-------- | :------- | :------------------------- |
| `__init__()` | `logging.getLogger()` | Your logging object. |
| `update_color_range()` | `HSV min & max Values` | Updates Mask Filter Parameters |
| `filter_points()` | `OpenCV Frame` | Filters Image and creates Binary Mask |
|`get_points()`| |Returns Joint Points as a Shuffled (Nx2) Shape List|

#### Eklem Tracker

| Parameter | Input Object     | Description                |
| :-------- | :------- | :------------------------- |
| `__init__()` | `logging.getLogger()` | Your logging object. |
| `get_all()` | | Returns all joint dictionaries as a list |
|`initialize_joints()`|`OpenCV Frame, color_detector`| Requests from user to define points on the image |
|`match`|`color_detector.get_points()`| Returns current joints position as a dictionary |
|`draw()`|`OpenCV Frame`| Draws joint on the frame and returns new frame |
|`get_joints()`| |Returns current joints positions as a dictionary|

## Demo

[![Click Here To See a Working Demo](https://img.youtube.com/vi/xavLNnz41uI/0.jpg)](https://www.youtube.com/watch?v=xavLNnz41uI)


## 🚀 About Me
I'm Sezer, a full stuck developer...

