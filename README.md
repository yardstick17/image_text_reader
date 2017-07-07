# image_text_reader

It's a very basic tool to read images , images formatted like a restaurant-menu.

### Tesseract-ocr
This tools need tesseract-ocr engine. Help yourself with this --
* https://github.com/tesseract-ocr/tesseract/wiki

###### OCR reads the text extracted image from the full image. [Click here](https://github.com/yardstick17/menu_parser/blob/master/boxed_image.jpg)

### Digital Menu
![Digital Image](images/digital_menu.jpg)]

### Original Image
![Original Image](images/sample_image.jpg)


## Command to use:
### Read from url

> PYTHONPATH='.' python3 read_image.py read_text_from_image_url -u https://marketplace.canva.com/MACHUlPU93Q/1/0/thumbnail_large/canva-peach-green-leaves-garden-vegetarian-pizza-menu-MACHUlPU93Q.jpg

```bash
[2017-07-07 16:20:34,119] INFO : Downloading image from url: https://marketplace.canva.com/MACHUlPU93Q/1/0/thumbnail_large/canva-peach-green-leaves-garden-vegeta
[2017-07-07 16:20:35,997] INFO : Saving file: /var/folders/cz/n3vkz7x91qs06nmm9byxxgz00000gr/T/tmpienrxu2c
[2017-07-07 16:20:35,997] INFO : Processing image for text Extraction
[2017-07-07 16:20:36,308] INFO : Removing noise and smoothening image
[2017-07-07 16:20:36,431] INFO : Reading the text inside the contour plotted
```


### Read from local image
> PYTHONPATH='.' python3 read_image.py read_text_from_local_image -f images/sample_image.jpg
```bash
[2017-07-07 16:32:38,862] INFO : Processing image for text Extraction
[2017-07-07 16:32:39,232] INFO : Removing noise and smoothening image
[2017-07-07 16:32:39,442] INFO : Reading the text inside the contour plotted
```

