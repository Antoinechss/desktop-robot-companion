from config import CONFIDENCE_THRESHOLD, PERSON_CLASS

class Detection:
    def __init__(self, coords, category, conf, metadata, imx500, picam2, frame_w, frame_h):
        """Creates a Detection object: bounding box + category + confidence"""
        self.category = category
        self.conf = conf
        self.box = imx500.convert_inference_coords(coords, metadata, picam2)

        # Compute the center of the box from its (x, y, w, h) coordinates
        x_center = self.box[0] + self.box[2]/2
        y_center = self.box[1] + self.box[3]/2
        cx_scaled, cy_scaled = (x_center / frame_w) * 2 - 1, (y_center / frame_h) * 2 - 1
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
        if score > CONFIDENCE_THRESHOLD
        and int(category) == PERSON_CLASS
    ]
    return frame_detections