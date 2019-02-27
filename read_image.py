# -*- coding: utf-8 -*-
import logging
import unicodedata

import click
import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from image_preprocessing.remove_noise import get_size_of_scaled_image
from image_preprocessing.remove_noise import process_image_for_ocr
from tesseract_interface import pytesser

THRESHOLD_FOR_INVERTED_IMAGE = 128
import tempfile


def extract_image_from_location(mask, x, y, w, h):
    temp_file = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg')
    temp_filename = temp_file.name
    im = mask[y:y + h, x:x + w]
    cv2.imwrite(temp_filename, im)
    size = 2 * w, 2 * h
    im = Image.open(temp_filename)
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(temp_filename, dpi=(300, 300))
    return pytesser.image_to_string(temp_filename, 6)


def extract_image_text(image):
    boxed_image = image.copy()
    img = image.copy()
    img2gray = img
    inv_img = (255 - img2gray)
    contours = find_possible_contours_in_image(inv_img)
    complete_image_text = read_contours_text(boxed_image, contours, img)
    cv2.imwrite('boxed_image.jpg', boxed_image)
    return complete_image_text


def read_contours_text(boxed_image, contours, img):
    """store on the location where it is located in the image. here it will be top-left pixel location as the key"""
    logging.info('Reading the text inside the contour plotted')
    image_text_dict = get_text_with_location(boxed_image, contours, img)
    write_as_digital_image(image_text_dict)
    list_of_text = []
    for key, value in sorted(image_text_dict.items()):
        list_of_text.append(value)
    return '\n'.join(list_of_text).strip()


def get_text_with_location(boxed_image, contours, img):
    image_text_dict = {}
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)
        # cv2.groupRectangles

        # draw rectangle around contour on original image

        # if w < 20 or h < 20:
        # 	continue
        if w > 300:
            continue

        cv2.rectangle(
            boxed_image, (x, y), (x + w + 10, y + h + 10),
            thickness=2,
            color=(0, 123, 123))
        """This writes the bounding box on image.
		"""

        box_read = extract_image_from_location(img, x, y, w, h)
        box_read = box_read.strip()
        image_text_dict[(x, y)] = box_read

    return image_text_dict


def find_possible_contours_in_image(inv_img):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 1))
    dilated = cv2.dilate(inv_img, kernel, iterations=5)  # dilate
    _, contours, hierarchy = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours
    cv2.imwrite('blurred_image.jpg', 255 - dilated)
    return contours


def read_image_from_file(filename):
    image = process_image_for_ocr(filename)
    image_text = extract_image_text(image)
    logging.info('Extracted Text:{}'.format(image_text))
    return image_text


def write_as_digital_image(image_text_dict):
    size = get_size_of_scaled_image('not required')
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Florentia-Thin-trial.ttf', 32)
    for location, text in image_text_dict.items():
        text = unicodedata.normalize('NFKD', text).encode(
            'ascii', 'ignore').lower().decode('utf-8')
        print(text)
        draw.text(location, text, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(img)
    img.save('digital_menu.jpg')


@click.group()
def main():
    return 0


@main.command()
@click.option('--filename', '-f', help='The input image with text to be read')
def read_text_from_local_image(filename):
    return read_image_from_file(filename)


@main.command()
@click.option('--url', '-u', help='The url of image')
def read_text_from_image_url(url):
    from api.app import download_image
    filename = download_image(url)
    return read_image_from_file(filename)


cli = click.CommandCollection(sources=[main])

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s : %(message)s', level=logging.INFO)
    cli()
