# -*- coding: utf-8 -*-
import logging
import os
from subprocess import PIPE
from subprocess import Popen

from clean_text.clean_text import CleanText

logger = logging.getLogger(__name__)

# All the PSM arguments as a variable name (avoid having to know them)
PSM_OSD_ONLY = 0
PSM_SEG_AND_OSD = 1
PSM_SEG_ONLY = 2
PSM_AUTO = 3
PSM_SINGLE_COLUMN = 4
PSM_VERTICAL_ALIGN = 5
PSM_UNIFORM_BLOCK = 6
PSM_SINGLE_LINE = 7
PSM_SINGLE_WORD = 8
PSM_SINGLE_WORD_CIRCLE = 9
PSM_SINGLE_CHAR = 10


class TesseractException(Exception):  # Raised when tesseract does not return 0
    pass


class PyTesseract:
    PROG_NAME = 'tesseract'
    TEMP_FILE = '/tmp/tmp'
    DEFAULT_EXTENSION = '.txt'

    def __init__(self, input_file, out_file, psm):
        """

		:param input_file:
		:param out_file:
		:param psm: Page segmentation modes:
					0    Orientation and script detection (OSD) only.
					1    Automatic page segmentation with OSD.
					2    Automatic page segmentation, but no OSD, or OCR.
					3    Fully automatic page segmentation, but no OSD. (Default)
					4    Assume a single column of text of variable sizes.
					5    Assume a single uniform block of vertically aligned text.
					6    Assume a single uniform block of text.
					7    Treat the image as a single text line.
					8    Treat the image as a single word.
					9    Treat the image as a single word in a circle.
					10    Treat the image as a single character.
					11    Sparse text. Find as much text as possible in no particular order.
					12    Sparse text with OSD.
					13    Raw line. Treat the image as a single text line,
										bypassing hacks that are Tesseract-specific.
		"""
        self.input_file = input_file
        self.output_file = out_file
        self.psm = psm

    def _read_image(self):
        args = [self.PROG_NAME, self.input_file,
                self.output_file]  # Create the arguments
        if self.psm:
            args.append('-psm')
            args.append(str(self.psm))
        proc = Popen(args, stdout=PIPE, stderr=PIPE)  # Open process
        ret = proc.communicate()  # Launch it
        code = proc.returncode
        if code != 0:
            raise TesseractException('Exception code: {}'.format(code))
        logger.debug('Output of image text is written in the file: %s',
                     self.output_file)
        return ret

    @property
    def filepath_with_extension(self):
        return self.output_file + self.DEFAULT_EXTENSION

    def read_text(self):
        self._read_image()
        with open(self.filepath_with_extension, 'r') as file:
            text = file.read()
            clean_text = CleanText(text).process()
        os.remove(self.filepath_with_extension)
        return clean_text


def image_to_string(file, psm=None):
    txt = PyTesseract(file, PyTesseract.TEMP_FILE, psm=psm).read_text()
    return txt
