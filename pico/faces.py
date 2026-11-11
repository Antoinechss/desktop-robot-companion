"""
Format : {'emotion_name': {'eye_l': [(x, y, w, h), ...],
                           'eye_r': [(x, y, w, h), ...],
                           'mouth':[(x,y,w,h), ...],
                           'background_color': st7789.COLOUR,
                           'add_on': {'coords': [...] 'color': ...}
                           }, ... }
"""

import st7789py as st7789

# --- Emotions library
EMOTIONS = {
    "neutral": {
        "eye_l": [(55, 60, 45, 70, st7789.WHITE)],
        "eye_r": [(140, 60, 45, 70, st7789.WHITE)],
        "mouth": [(85, 170, 70, 10, st7789.WHITE)],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "wink": {
        "eye_l": [(55, 80, 45, 5, st7789.WHITE)],
        "eye_r": [(140, 80, 45, 70, st7789.WHITE)],
        "mouth": [(85, 170, 70, 10, st7789.WHITE)],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "angry": {
        "eye_l": [
            (55, 60, 15, 70, st7789.RED),
            (70, 70, 15, 60, st7789.RED),
            (85, 80, 15, 50, st7789.RED),
        ],
        "eye_r": [
            (140, 80, 15, 50, st7789.RED),
            (155, 70, 15, 60, st7789.RED),
            (170, 60, 15, 70, st7789.RED),
        ],
        "mouth": [
            (95, 170, 50, 10, st7789.RED),
            (85, 180, 10, 10, st7789.RED),
            (145, 180, 10, 10, st7789.RED),
        ],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "sad": {
        "eye_l": [
            (55, 80, 15, 50, st7789.WHITE),
            (70, 70, 15, 60, st7789.WHITE),
            (85, 60, 15, 70, st7789.WHITE),
        ],
        "eye_r": [
            (140, 60, 15, 70, st7789.WHITE),
            (155, 70, 15, 60, st7789.WHITE),
            (170, 80, 15, 50, st7789.WHITE),
        ],
        "mouth": [
            (95, 170, 50, 10, st7789.WHITE),
            (85, 180, 10, 10, st7789.WHITE),
            (145, 180, 10, 10, st7789.WHITE),
        ],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "happy": {
        "eye_l": [(55, 60, 45, 55, st7789.WHITE)],
        "eye_r": [(140, 60, 45, 55, st7789.WHITE)],
        "mouth": [
            (95, 170, 50, 10, st7789.WHITE),
            (85, 160, 10, 10, st7789.WHITE),
            (145, 160, 10, 10, st7789.WHITE),
        ],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "suspicious": {
        "eye_l": [(55, 80, 45, 10, st7789.WHITE)],
        "eye_r": [(140, 80, 45, 10, st7789.WHITE)],
        "mouth": [(85, 170, 70, 10, st7789.WHITE)],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "surprise": {
        "eye_l": [(55, 60, 45, 70, st7789.WHITE)],
        "eye_r": [(140, 60, 45, 70, st7789.WHITE)],
        "mouth": [(100, 160, 40, 30, st7789.WHITE)],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "sleeping": {
        "eye_l": [(55, 80, 45, 3, st7789.CYAN)],
        "eye_r": [(140, 80, 45, 3, st7789.CYAN)],
        "mouth": [(85, 173, 70, 4, st7789.CYAN)],
        "background_color": st7789.BLACK,
        "add_on": None,
    },
    "blush": {
        "eye_l": [(55, 60, 45, 30, st7789.WHITE)],
        "eye_r": [(140, 60, 45, 30, st7789.WHITE)],
        "mouth": [
            (95, 170, 50, 10, st7789.WHITE),
            (85, 160, 10, 10, st7789.WHITE),
            (145, 160, 10, 10, st7789.WHITE),
        ],
        "background_color": st7789.BLACK,
        "add_on": [
            (35, 130, 30, 14, st7789.color565(255, 110, 150)),
            (175, 130, 30, 14, st7789.color565(255, 110, 150)),
        ],
    },
}

CLOSED_EYES = [
    (55, 93, 45, 4),
    (140, 93, 45, 4),
]  # Closed eyes used for blinking (same for every emotion)


def compute_face(emotion: str, gaze_dx: int, blinking: bool):
    """Returns a list of (x, y, w, h, color) tuples for each rectangle to draw"""
    rects = []
    emo_params = EMOTIONS[emotion]

    # --- Eyes
    if blinking:
        c_eye = emo_params["eye_l"][0][4]
        for r in CLOSED_EYES:
            x_eye, y_eye, w_eye, h_eye = r
            x_eye += gaze_dx
            rects.append((x_eye, y_eye, w_eye, h_eye, c_eye))

    else:
        for r in emo_params["eye_l"]:
            x_eye_l, y_eye_l, w_eye_l, h_eye_l, c_eye_l = r
            x_eye_l += gaze_dx
            rects.append((x_eye_l, y_eye_l, w_eye_l, h_eye_l, c_eye_l))
        for r in emo_params["eye_r"]:
            x_eye_r, y_eye_r, w_eye_r, h_eye_r, c_eye_r = r
            x_eye_r += gaze_dx
            rects.append((x_eye_r, y_eye_r, w_eye_r, h_eye_r, c_eye_r))

    # --- Mouth
    for r in emo_params["mouth"]:
        x_mouth, y_mouth, w_mouth, h_mouth, c_mouth = r
        x_mouth += int(gaze_dx * 0.4)
        rects.append((x_mouth, y_mouth, w_mouth, h_mouth, c_mouth))

    # --- Add-ons
    if emo_params["add_on"] is not None:
        for a in emo_params["add_on"]:
            rects.append(a)

    return rects


def draw_face(tft, old_rects, new_rects, bg_color):
    """
    Draws the new face by checking if preceeding face has matches 
    with new one to avoid full erase and redraw
    returns the new rectangles displayed
    """
    for r in old_rects:
        if r not in new_rects:
            tft.fill_rect(r[0], r[1], r[2], r[3], bg_color)
    for r in new_rects:
        if r not in old_rects:
            tft.fill_rect(r[0], r[1], r[2], r[3], r[4])

    return new_rects
