import numpy as np
from math_functions import *


# keypoint labels
"""
    0. Nose
    1. Left Eye
    2. Right Eye
    3. Left Ear
    4. Right Ear
    5. Left Shoulder
    6. Right Shoulder
    7. Left Elbow
    8. Right Elbow
    9. Left Wrist
    10. Right Wrist
    11. Left Hip
    12. Right Hip
    13. Left Knee
    14. Right Knee
    15. Left Ankle
    16. Right Ankle
"""

# Takes in a box and its keypoints and returns a number representing the pose
def get_pose(box, keypoints):
    """
    poses:
    0. Standing: default pose
    1. crouching:
    2. kneeling:
    3. sitting:
    4. laying:
    5: bending
    """

    # width to height ratio of box
    box_ratio = (box[2] - box[0]) / (box[3] - box[1])

    if box_ratio < 1.75:
        crouch_bend = is_crouching_or_bending(box,keypoints)

        if crouch_bend == 1:
            return 1
        elif crouch_bend == 2:
            return 2
        elif is_kneeling(box,keypoints):
            return 3
        elif is_sitting(box,keypoints):
            return 4
        else:
            return 0
    else:
        return 5

# returns 1 if crouching or 2 if bending or -1 if neither
def is_crouching_or_bending(box,keypoints):
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]

    left_hip = keypoints[11]
    right_hip = keypoints[12]

    left_knee = keypoints[13]
    right_knee = keypoints[14]

    left_ankle = keypoints[15]
    right_ankle = keypoints[16]

    # get hip angles
    hip_angle_l = calculate_angle(left_shoulder, left_hip, left_knee)
    hip_angle_r = calculate_angle(right_shoulder, right_hip, right_knee)

    # get knee angles
    knee_angle_l = calculate_angle(left_hip, left_knee, left_ankle)
    knee_angle_r = calculate_angle(right_hip, right_knee, right_ankle)


    # determine if crouching

    # if left side hip and knee angles are small
    if hip_angle_l < 85:
        if knee_angle_l < 85:
            return 1
        return 2

    # if left side hip and knee angles are small
    if hip_angle_r < 85:
        if knee_angle_r < 85:
            return 1
        return 2
    return -1


def is_kneeling(box,keypoints):
    # get location of keypoints
    left_knee_height = keypoints[13][1]
    right_knee_height = keypoints[14][1]

    left_ankle_height = keypoints[15][1]
    right_ankle_height = keypoints[16][1]


    # determine if kneeling
    if (left_ankle_height - left_knee_height < 0.1) and left_knee_height > 0.85 :
        return True
    if (right_ankle_height - right_knee_height < 0.1) and right_knee_height > 0.85 :
        return True


    return False

def is_sitting(box,keypoints):
    # get location of keypoints
    hips = [np.mean([keypoints[11][0], keypoints[12][0]]), np.mean([keypoints[11][1], keypoints[12][1]])]
    ankles = [np.mean([keypoints[15][0], keypoints[16][0]]), np.mean([keypoints[15][1], keypoints[16][1]])]

    hips_height = hips[1]
    ankles_height = ankles[1]

    # determine if sitting
    if (ankles_height - hips_height) < 0.2 and hips_height > 0.75:
        return True

    return False
