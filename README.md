# Menu Parser

It's a very basic command line tool to read images , images formatted like a restaurant-menu. It outputs the text part excluding the numerical part and special character.

### Commands

```sh
extract_dish --help 

extract_dish 					    ( reads a default image)	

extract_dish file_path_to_image		(reads image at path file_path_to_image)
```

### Tesseract-ocr
This tools need tesseract-ocr engine. Help yourself with this --
* https://github.com/tesseract-ocr/tesseract/wiki

### OCR reads the text extracted image from the full image. [Click here](https://github.com/yardstick17/menu_parser/blob/master/boxed_image.jpg)
