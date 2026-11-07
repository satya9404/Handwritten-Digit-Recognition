import cv2
import numpy as np


def preprocess_image(image_path):

    # 1. Read image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image")

    # 2. Detect coloured handwriting
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)

    color_mask = (
        (h >= 90) &
        (h <= 170) &
        (s >= 20) &
        (v <= 245)
    ).astype(np.uint8) * 255

    # 3. Choose preprocessing based on handwriting type
    if cv2.countNonZero(color_mask) > 20:

        # Blue/purple handwriting
        digit_mask = color_mask

        kernel = np.ones((3, 3), np.uint8)

        digit_mask = cv2.morphologyEx(
            digit_mask,
            cv2.MORPH_CLOSE,
            kernel
        )

    else:

        # Black handwriting from drawing canvas
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        _, digit_mask = cv2.threshold(
            blurred,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

    # 4. Find handwriting boundaries
    points = cv2.findNonZero(digit_mask)

    if points is None:
        raise ValueError("No handwriting detected")

    x, y, w, height = cv2.boundingRect(points)

    digit = digit_mask[y:y + height, x:x + w]

    # 5. Resize while maintaining aspect ratio
    scale = 20 / max(height, w)

    new_width = max(1, int(w * scale))
    new_height = max(1, int(height * scale))

    resized = cv2.resize(
        digit,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    # 6. Create 28x28 MNIST image
    canvas = np.zeros((28, 28), dtype=np.uint8)

    x_offset = (28 - new_width) // 2
    y_offset = (28 - new_height) // 2

    canvas[
        y_offset:y_offset + new_height,
        x_offset:x_offset + new_width
    ] = resized

    # 7. Normalize
    canvas = canvas.astype("float32") / 255.0

    # 8. CNN input format
    return canvas.reshape(1, 28, 28, 1)