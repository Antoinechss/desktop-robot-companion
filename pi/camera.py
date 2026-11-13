from picamera2.devices import IMX500
from picamera2.devices.imx500 import NetworkIntrinsics
from picamera2 import Picamera2


def setup_camera(model, task="object detection"):
    """Load a model on the IMX500 and start the camera.
    task: "object detection" or "pose estimation"."""
    imx500 = IMX500(model)
    intrinsics = imx500.network_intrinsics
    if not intrinsics:
        intrinsics = NetworkIntrinsics()
        intrinsics.task = task
    elif intrinsics.task != task:
        raise ValueError(f"Network is not a {task} task")

    intrinsics.update_with_defaults()

    picam2 = Picamera2(imx500.camera_num)
    cam_config = picam2.create_preview_configuration(
        controls={"FrameRate": intrinsics.inference_rate}, buffer_count=12
    )
    imx500.show_network_fw_progress_bar()
    picam2.start(cam_config, show_preview=False)
    frame_w, frame_h = picam2.camera_configuration()["main"]["size"]

    if intrinsics.preserve_aspect_ratio:
        imx500.set_auto_aspect_ratio()

    return imx500, picam2, intrinsics, frame_w, frame_h
