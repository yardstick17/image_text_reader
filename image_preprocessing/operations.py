import cv2


def mean_image_pixel_value(image):
    size = 128, 128
    resized_image = cv2.resize(image, size)
    return resized_image.mean()
