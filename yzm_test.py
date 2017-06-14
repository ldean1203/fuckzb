import pytesseract

from PIL import Image

image = Image.open('static/img/yzm.jpg')

vcode = pytesseract.image_to_string(image)

print (vcode)