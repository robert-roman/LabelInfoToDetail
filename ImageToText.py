import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def imageToText(img):
    myconfig = r"--psm 6 --oem 3"
    ##todo change back to romanian after validation
    # return pytesseract.image_to_string(image=img, lang="ron", config=myconfig)
    return pytesseract.image_to_string(image=img, lang="eng", config=myconfig)

# from PIL import Image
# image = Image.open( "Images\img_6.png")
# print(imageToText(image))