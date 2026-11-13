import numpy as np
from config import CONFIDENCE_THRESHOLD, PERSON_CLASS, POSE_THRESHOLD, KP_THRESHOLD, POSE_SIZE_H_W
from picamera2.devices.imx500.postprocess_highernet import postprocess_higherhrnet

H, W = POSE_SIZE_H_W

class Face: 
    def __init__(
            self, center, score
    ): 
        self.center = center # (x, y) in [-1, 1]
        self.score = score

class Detection:
    def __init__(
        self, coords, category, conf, metadata, imx500, picam2, frame_w, frame_h
    ):
        """Creates a Detection object: bounding box + category + confidence"""
        self.category = category
        self.conf = conf
        self.box = imx500.convert_inference_coords(coords, metadata, picam2)

        # Compute the center of the box from its (x, y, w, h) coordinates
        x_center = self.box[0] + self.box[2] / 2
        y_center = self.box[1] + self.box[3] / 2
        cx_scaled, cy_scaled = (x_center / frame_w) * 2 - 1, (
            y_center / frame_h
        ) * 2 - 1
        self.center = (cx_scaled, cy_scaled)


def parse_detections(metadata: dict, imx500, picam2, intrinsics, frame_w, frame_h):
    """Parse the output tensor into a number of detected objects, scaled to the ISP output."""
    bbox_normalization = intrinsics.bbox_normalization
    bbox_order = intrinsics.bbox_order

    # Extract arrays of (boxes, scores, classes) for the frame
    np_outputs = imx500.get_outputs(metadata, add_batch=True)
    input_w, input_h = imx500.get_input_size()
    if np_outputs is None:
        return []
    else:
        boxes, scores, classes = np_outputs[0][0], np_outputs[1][0], np_outputs[2][0]
        if bbox_normalization:
            boxes = boxes / input_h
        if bbox_order == "xy":
            boxes = boxes[:, [1, 0, 3, 2]]

    # Build list of detected people in the frame
    frame_detections = [
        Detection(box, category, score, metadata, imx500, picam2, frame_w, frame_h)
        for box, score, category in zip(boxes, scores, classes)
        if score > CONFIDENCE_THRESHOLD and int(category) == PERSON_CLASS
    ]
    return frame_detections


def parse_poses(metadata: dict, imx500): 
    poses = []
    
    # 1. Fetch raw outputs 
    np_outputs = imx500.get_outputs(metadata, add_batch=True)
    if np_outputs is None: 
        return []
    
    # 2. parser 
    keypoints, scores, boxes = postprocess_higherhrnet(
        outputs=np_outputs,
        img_size=POSE_SIZE_H_W,
        img_w_pad=(0, 0),
        img_h_pad=(0, 0),
        detection_threshold=POSE_THRESHOLD,
        network_postprocess=True,
    )
    if scores is None or len(scores) == 0:
        return []

    # 3. reshape 
    kp = np.reshape(np.stack(keypoints, axis=0), (len(scores), 17, 3)) # len(scores) = nb of people detected 
    for i in range(len(scores)): 
        nose_x, nose_y, nose_conf = kp[i][0]
        left_eye_x, left_eye_y, left_eye_conf = kp[i][1]
        right_eye_x, right_eye_y, right_eye_conf = kp[i][2]

        if nose_conf > KP_THRESHOLD: 
            face_point_x, face_point_y = nose_x, nose_y
        elif (right_eye_conf > KP_THRESHOLD and left_eye_conf > KP_THRESHOLD): 
            face_point_x, face_point_y = (left_eye_x + right_eye_x)/2, (left_eye_y + right_eye_y)/2
        else: 
            continue

        # Normalize 
        face_point_x_scaled, face_point_y_scaled = face_point_x / W * 2 - 1, face_point_y / H * 2 - 1

        poses.append(Face((face_point_x_scaled, face_point_y_scaled), scores[i]))

    return poses

