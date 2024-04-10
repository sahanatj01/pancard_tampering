from app import app
from Flask import request, render_template
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

app.config['Initial_File_Uploads'] = 'app/static/uploads'
app.config['existing_File'] = 'app/static/original'
app.config['Generated_File'] = 'app/static/generated'

@app.route("/", methods = []'GET', 'POST]')
def index():
    if request.method == 'GET':
        return render_template("index.html")
    
    if request.method =='POST':
        file_upload = request.files['file_upload']
        filename = file_upload.filename


        original = original.resize((250,160))
print(original.size)
tampered = tampered.resize((250,160))
print(tampered.size)
original.save("pan_card_tampering/image/original.png")
tampered.save("pan_card_tampering/image/tampered.png")
original
tampered


#load the images
original = cv2.imread("pan_card_tampering/image/original.png")
tampered = cv2.imread("pan_card_tampering/image/tampered.png")


#convert to greyscale
original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
tampered_gray = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)

#Compute structural similarity Index (SSIM)
(score,diff)=structural_similarity(original_gray,tampered_gray, full=True)
diff = (diff*255).astype("uint8")
print("SSIM:{}".format(score))

#calculating threshold and contours of images
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

#loop over the contours

for c in cnts:
    (x,y,w,h) = cv2.boundingRect(c)
    cv2.rectangle(original, (x,y), (x+w, y+h), (0, 0, 255), 2)
    cv2.rectangle(tampered, (x,y), (x+w, y+h), (0, 0, 255), 2)

#display original image with contour
print('original Format image')
Image.fromarray(original)

#display tampered image with contour
print('tampered Format image')
Image.fromarray(tampered)

#display difference image with black
print("Different image")
Image.fromarray(diff)

#display threshold with white
print("threshold image")
Image.fromarray(thresh)