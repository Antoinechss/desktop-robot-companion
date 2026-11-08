import sys
from functools import lru_cache

from picamera2 import Picamera2
from picamera2.devices import IMX500
from picamera2.devices.imx500 import NetworkIntrinsics


# --- Model Parameters
MODEL = "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"
CONFIDENCE_THRESHOLD = 0.5
PERSON_CLASS = 0

class Detection:
    def __init__(self, coords, category, conf, metadata):
        """Creates a Detection object: bounding box + category + confidence"""
        self.category = category
        self.conf = conf
        self.box = imx500.convert_inference_coords(coords, metadata, picam2)

        # Compute the center of the box from its (x, y, w, h) coordinates
        x_center = self.box[0] + self.box[2]/2
        y_center = self.box[1] + self.box[3]/2
        self.center = (x_center, y_center)


def parse_detections(metadata: dict):
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
        Detection(box, category, score, metadata) 
        for box, score, category in zip(boxes, scores, classes) 
        if score > CONFIDENCE_THRESHOLD
        and int(category) == PERSON_CLASS
    ]
    return frame_detections

if __name__ == "__main__":
    # Calling model & intrinsic elements of imx500

    imx500 = IMX500(MODEL)
    intrinsics = imx500.network_intrinsics
    if not intrinsics:
        intrinsics = NetworkIntrinsics()
        intrinsics.task = "object detection"
    elif intrinsics.task != "object detection":
        print("Network is not an object detection task", file=sys.stderr)
        exit()
        
    intrinsics.update_with_defaults()

    # Configure Camera  
    picam2 = Picamera2(imx500.camera_num)
    config = picam2.create_preview_configuration(controls={"FrameRate": intrinsics.inference_rate}, buffer_count=12)
    imx500.show_network_fw_progress_bar()
    picam2.start(config, show_preview=False)
    frame_w, frame_h = picam2.camera_configuration()["main"]["size"]  

    if intrinsics.preserve_aspect_ratio:
        imx500.set_auto_aspect_ratio()

    while True:
        frame_detections = parse_detections(picam2.capture_metadata())
        for detection in frame_detections: 
            cx, cy = detection.center
            # Normalize position between -1, 1
            cx_scaled, cy_scaled = (cx / frame_w) * 2 - 1, (cy / frame_h) * 2 - 1
            print(f"person  x={cx_scaled:+.2f}  y={cy_scaled:+.2f}  conf={detection.conf:.2f}")




