from PIL import Image
import pytesser3
image = Image.open('yzm.jpg')
print(pytesser3.image_file_to_string('yzm.jpg'))
print (pytesser3.image_to_string(image))