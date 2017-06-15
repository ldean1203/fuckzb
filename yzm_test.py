from pytesser3 import *
im = Image.open('yzm.jpg')
text = image_to_string(im)
print( "Using image_to_string(): ")
print(text)
text = image_file_to_string('fonts_test.png', graceful_errors=True)
print("Using image_file_to_string():")
print(text)