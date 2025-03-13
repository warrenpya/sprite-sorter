import os
import shutil
from ultralytics import YOLO
from get_pose import get_pose

# Predicts all images in a directory
def predict(model):
    results = model.predict(
        source=source_dir,
        conf=0.84,
        save=True,
        )

    return results

# Ensures input path is good, creates output folder
def set_paths():
    # alert and quit if input directory does not exist
    if not os.path.exists(source_dir):
        return "Input directory does not exist"

    extensions = ['.bmp', '.dng', '.jpeg', '.jpg', '.mpo',
                        '.png', '.tif', '.tiff', '.webp', '.pfm', '.HEIC','.db']

    # ensure input folder has valid files
    for root, dirs, files in os.walk(source_dir):
        if len(files) == 0:
            return "Input directory cannot be empty"
        if dirs:
            return "Input directory cannot contain subdirectories"
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in extensions:
                return f"Input directory has file(s) of the incorrect type of {file_extension}"

    # if output directory already exists, delete it
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # create output directory
    try:
        os.makedirs(output_dir)
    except:
        return "Error creating output directory"
        

"""
returns category in [x,y] where x is sprite type and y is pose id

sprite type: integer representing number of people, or 0 if ball
pose id: integer representing type of pose in pose_keys
"""
def get_category(results):
    boxes = results.boxes.xyxy
    keypoints_set = results.keypoints.xy
    num_boxes = len(boxes)

    # if no boxes
    if num_boxes == 0:
        return [0,None]

    # if one box, check it has all keypoints except elbows/wrists
    one_box_is_player = True
    # print(f"\ncalculating if box is player:")
    if num_boxes == 1:
        # check if head exists
        has_head = False
        for j in range(0,5):
            if keypoints_set[0][j][0] > 0.0001:
                has_head = True
        if not has_head:
            one_box_is_player = False
        # check if all limbs are there
        for j in [5,6,11,12,13,14,15,16]:
            # print(f"is kp {j}0?")
            if keypoints_set[0][j][0] < 0.0001:
                # print(f"yes")
                one_box_is_player = False
                break
    # print(f"box is player?: {one_box_is_player}")
    # if image has one box
    if num_boxes == 1:
        # if that box has all limbs
        if one_box_is_player:
            keypoints_0_normalized = normalize_keypoints_by_box(keypoints_set[0],boxes[0])
            # print(f"\ngetting pose for image {os.path.basename(results.path)}")
            return [num_boxes, get_pose(boxes[0],keypoints_0_normalized)]
        # if that box does not have all limbs
        else:
            return [num_boxes, -1]

    # if image is more than one player
    if num_boxes > 1:
        return [num_boxes, None]





# normalize keypoints to box size
def normalize_keypoints_by_box(keypoints,box):
    keypoints_normalized = []

    for i in range(len(keypoints)):
        kp_x = float(keypoints[i][0])
        kp_y = float(keypoints[i][1])

        box_x1 = float(box[0])
        box_y1 = float(box[1])
        box_w = float(box[2] - box[0])
        box_h = float(box[3] - box[1])

        if kp_x < 0.0001 or kp_y < 0.0001:
            keypoint = [0, 0]
        else:
            keypoint = [(kp_x - box_x1) / box_w, (kp_y - box_y1) / box_h]
        keypoints_normalized.append(keypoint)

    return keypoints_normalized


# Moves image to output directory based on class of image
def move_img_by_category(img_path, category):
    num_boxes = category[0]
    pose = category[1]

    # determine sub folder name
    dir_name = ""

    # no boxes
    if num_boxes == 0 or (num_boxes == 1 and pose == -1):
        dir_name += f"no_detection"

    # 1 box and has a pose
    elif num_boxes == 1 and pose != -1:
        dir_name += f"1_player_{pose_keys[pose]}"

    # more than 1 box
    elif num_boxes > 1:
        dir_name += f"{num_boxes}_players"

    # create sub folder
    output_sub_dir = os.path.join(output_dir, dir_name)
    if not os.path.exists(output_sub_dir):
        os.makedirs(output_sub_dir)

    # copy image to subfolder
    shutil.copy(img_path, output_sub_dir)

# sort images from source_dir into output_dir
def sort(source_dir_param,output_dir_param):
    # set input/output paths
    global source_dir, output_dir
    source_dir = source_dir_param
    output_dir = output_dir_param
    set_paths_error = set_paths()
    if set_paths_error:
        return set_paths_error

    # yolo models from fastest to slowest
    models = ["YOLO11n","YOLO11s","YOLO11m","YOLO11l","YOLO11x"]

    # run model
    model = YOLO(f"{models[-1]}-pose.pt")
    results = predict(model)

    # sort results
    i = 1
    len_results = len(results)
    for r in results:
        category = get_category(r)
        move_img_by_category(r.path, category)
        print(f"Sorted image {i}/{len_results}")
        i += 1
    print("Sorting completed")


source_dir = ""
output_dir = ""
pose_keys = ["standing", "crouching", "bending", "kneeling", "sitting", "laying"]



