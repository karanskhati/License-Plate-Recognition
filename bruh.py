# -*- coding: utf-8 -*-
"""ps2 ki maa.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13S-rHjqSNlz8iIaZapRjuwo8Lun1hrr-
"""



from google.colab import drive
drive.mount("/content/gdrive")
# !sudo apt install tesseract-ocr
# !pip install pytesseract
# import pytesseract
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image
import keras

# !unzip "/content/gdrive/MyDrive/mosaic/karan_model/ps2/plates.zip"

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

def PlateDetect(img):
    net =cv2.dnn.readNet('/content/gdrive/MyDrive/PS2_Mosaic/yoloseg/backup/darknet-yolov3_last.weights','/content/gdrive/MyDrive/PS2_Mosaic/yoloseg/darknet-yolov3.cfg')
    classes=[]
    with open('/content/gdrive/MyDrive/PS2_Mosaic/yoloseg/classes.names','r') as f:
        classes=f.read().splitlines()

    for classi in classes:
        print(classi)
    # cap=cv2.VideoCapture(0)

    if img is None:
        print("No Image Found")
        return None
    height,width,_= img.shape
    blob=cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop=False)
    net.setInput(blob)
    output_layer_names=net.getUnconnectedOutLayersNames()
    layerOutputs =net.forward(output_layer_names)
    # while True:
    #     ret,img = cap.read()
    #     height,width,_= img.shape
    #     blob=cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop=False)
    #     net.setInput(blob)
    #     output_layer_names=net.getUnconnectedOutLayersNames()
    #     layerOutputs =net.forward(output_layer_names)
        
    boxes=[]
    confidences=[]
    class_ids=[]
        
    for output in layerOutputs:
        for detection in output:
            scores=detection[5:]
            class_id=np.argmax(scores)
            confidence=scores[class_id]
            if confidence>-1 :
                centre_x=int(detection[0]*width)
                centre_y=int(detection[1]*height)
                w=int (detection[2]*width)
                #print(w)
                h=int (detection[3]*height)
                x=int (centre_x-w/2)
                y=int (centre_y-h/2)
                boxes.append([x,y,w,h,confidence])
                confidences.append((float(confidence)))
                class_ids.append(class_id)
    
    indexes=cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)
    confi=max(confidences)
    indexes1 = np.asarray(indexes)
    font=cv2.FONT_HERSHEY_PLAIN
    colors= np.random.uniform( 0, 255, size = ( len( boxes ),3))
    arr=np.array([[0,0,0,0]])

    for i in indexes1.flatten():
        print(i)
        x, y, w, h,_ = boxes[i]
        arr=np.insert(arr,[1],[x,y,w,h],axis=0)
        # print(x,y,w,h)
        # label=str(classes[class_ids[i]])
        # confidence=str(round(confidences[i],2))
        # color=colors[i]
        # img2=img.copy()[y:y+h,x:x+w]
        # cv2_imshow(img2)
        # cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
        # cv2.putText(img,label+" "+ confidence,(x,y+20),font,2,(255,255,255),2)
    
    sortedArr = arr[arr[:,0].argsort()]
    # print(" ")
    # print(sortedArr)
    letters=list()
    for x,y,w,h in sortedArr:
      if x==0 and y==0 and w==0 and h==0:
        continue
      else:
        img2=img.copy()[y-1:y+h+1,x-1:x+w+1]
        letters.append(img2)
    # print(sortedArr.shape)
    # cv2_imshow(img)
    cv2.waitKey(0)



    cv2.destroyAllWindows()
    return letters

# img=cv2.imread('/content/indian_plates/ (7).png')
# cv2_imshow(img)
# img2=PlateDetect(img)
# for letter in img2:
#   cv2_imshow(letter)
#   print(letter.shape)

# img_=img2[2]
# cv2_imshow(img_)

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=2.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def process(img_):
    cv2_imshow(img_)
    #Resize
    if (img_.shape[0]>img_.shape[1]):
      resize_parm=(100/img_.shape[0])

    else:
      resize_parm=(100/img_.shape[1])

    resize_width=(int)(resize_parm*img_.shape[1])
    resize_height=(int)(resize_parm*img_.shape[0])
    crop_img = cv2.resize(img_ , (resize_width, resize_height))
    #cv2_imshow(crop_img)

    sharped_img=unsharp_mask(crop_img)    
    #cv2_imshow(sharped_img)

    gray = cv2.cvtColor(sharped_img, cv2.COLOR_BGR2GRAY)
    #cv2_imshow(gray)

    # Maximizing te constarst
    h,w=gray.shape
    imgTopHat = np.zeros((h, w, 1), np.uint8)
    imgBlackHat = np.zeros((h, w, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    impv_img=imgGrayscalePlusTopHatMinusBlackHat
    #cv2_imshow(impv_img)

    bw_img = cv2.adaptiveThreshold(impv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 199, 5)
    #cv2_imshow(bw_img)
    #print(bw_img.shape[0]*bw_img.shape[1])



    noise=(bw_img.shape[0]*bw_img.shape[1]*4)/1000
    print(noise)

    ret, binary_map = cv2.threshold(bw_img,127,255,0)

    # do connected components processing
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_map, None, None, None, 8, cv2.CV_32S)

    #get CC_STAT_AREA component as stats[label, COLUMN] 
    areas = stats[1:,cv2.CC_STAT_AREA]

    dn2_img = np.zeros((labels.shape), np.uint8)

    for i in range(0, nlabels - 1):
        if areas[i] >= noise:   #keep
            dn2_img[labels == i + 1] = 255
    #cv2_imshow(dn2_img)  #"Result", 



    # Perform connected components analysis on the thresholded image and
    # initialize the mask to hold only the components we are interested in
    _, labels = cv2.connectedComponents(dn2_img)
    mask = np.zeros(dn2_img.shape, dtype="uint8")
    # Set lower bound and upper bound criteria for characters
    total_pixels = dn2_img.shape[0] * dn2_img.shape[1]
    lower = total_pixels // 18 # heuristic param, can be fine tuned if necessary
    upper = total_pixels  # heuristic param, can be fine tuned if necessary
    # Loop over the unique components
    for (i, label) in enumerate(np.unique(labels)):
        # If this is the background label, ignore it
        if label == 0:
            continue
          # Otherwise, construct the label mask to display only connected component
        # for the current label
        labelMask = np.zeros(dn2_img.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
          # If the number of pixels in the component is between lower bound and upper bound, 
        # add it to our mask
        if numPixels > lower and numPixels < upper:
            mask = cv2.add(mask, labelMask)
    #mask2=cv2.dilate(mask,(5,5),iterations=2)
    #cv2_imshow(mask)


    image=mask.copy()

    if image.shape[0]>image.shape[1]:
      h=(image.shape[0]-image.shape[1])/2
      added_image = cv2.copyMakeBorder(image,0,0,int (h),int (h),cv2.BORDER_CONSTANT, None, 0)
    else:
      h=(image.shape[1]-image.shape[0])/2
      added_image = cv2.copyMakeBorder(image,int (h),int (h),0,0,cv2.BORDER_CONSTANT, None, 0)

    #cv2_imshow(added_image)

    roi=added_image.copy()
    image_f = cv2.copyMakeBorder(roi,int (.1*roi.shape[0]),int (.1*roi.shape[0]),int (.1*roi.shape[1]),int (.1*roi.shape[1]),cv2.BORDER_CONSTANT, None, 0)
    cv2_imshow(image_f)

    return image_f

def pred(image,model):
    mapping={
        0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"A",11:"B",12:"C",13:"D",14:"E"
        ,15:"F",16:"G",17:"H",18:"I",19:"J",20:"K",21:"L",22:"M",23:"N",24:"O",25:"P",26:"Q",27:"R",28:"S",29:"T"
        ,30:"U",31:"V",32:"W",33:"X",34:"Y",35:"Z"}
    character = cv2.cvtColor(image , cv2.COLOR_GRAY2BGR)
    x=cv2.resize(character,(32,32))
    x = np.expand_dims(x, axis=0)
    x.shape
    ans=model.predict(x)
    predicted=mapping[np.argmax(ans)]
    return predicted

# resize_parm=1

# if (img_.shape[0]>img_.shape[1]):
#   resize_parm=(32/img_.shape[0])

# else:
#   resize_parm=(32/img_.shape[1])

# resize_width=(int)(resize_parm*img_.shape[1])
# resize_height=(int)(resize_parm*img_.shape[0])
# crop_img = cv2.resize(img_ , (resize_width, resize_height))
# cv2_imshow(crop_img)

# def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=2.0, threshold=0):
#     """Return a sharpened version of the image, using an unsharp mask."""
#     blurred = cv2.GaussianBlur(image, kernel_size, sigma)
#     sharpened = float(amount + 1) * image - float(amount) * blurred
#     sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
#     sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
#     sharpened = sharpened.round().astype(np.uint8)
#     if threshold > 0:
#         low_contrast_mask = np.absolute(image - blurred) < threshold
#         np.copyto(sharpened, image, where=low_contrast_mask)
#     return sharpened

# sharped_img=unsharp_mask(crop_img)    
# cv2_imshow(sharped_img)

#plate_img=cv2.convertScaleAbs(img,alpha=(255.0))
# gray = cv2.cvtColor(sharped_img, cv2.COLOR_BGR2GRAY)
# cv2_imshow(gray)

# Maximizing te constarst

# h,w=gray.shape
# imgTopHat = np.zeros((h, w, 1), np.uint8)
# imgBlackHat = np.zeros((h, w, 1), np.uint8)

# structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
# imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

# imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
# imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

# impv_img=imgGrayscalePlusTopHatMinusBlackHat
# cv2_imshow(impv_img)

# bw_img = cv2.adaptiveThreshold(impv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 199, 5)
# cv2_imshow(bw_img)
# print(bw_img.shape[0]*bw_img.shape[1])

# noise=(bw_img.shape[0]*bw_img.shape[1]*4)/1000
# print(noise)

# ret, binary_map = cv2.threshold(bw_img,127,255,0)

# # do connected components processing
# nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_map, None, None, None, 8, cv2.CV_32S)

# #get CC_STAT_AREA component as stats[label, COLUMN] 
# areas = stats[1:,cv2.CC_STAT_AREA]

# dn2_img = np.zeros((labels.shape), np.uint8)

# for i in range(0, nlabels - 1):
#     if areas[i] >= noise:   #keep
#         dn2_img[labels == i + 1] = 255
# cv2_imshow(dn2_img)  #"Result",

# # Perform connected components analysis on the thresholded image and
# # initialize the mask to hold only the components we are interested in
# _, labels = cv2.connectedComponents(dn2_img)
# mask = np.zeros(dn2_img.shape, dtype="uint8")
# # Set lower bound and upper bound criteria for characters
# total_pixels = dn2_img.shape[0] * dn2_img.shape[1]
# lower = total_pixels // 50 # heuristic param, can be fine tuned if necessary
# upper = total_pixels  # heuristic param, can be fine tuned if necessary
# # Loop over the unique components
# for (i, label) in enumerate(np.unique(labels)):
#     # If this is the background label, ignore it
#     if label == 0:
#         continue
#       # Otherwise, construct the label mask to display only connected component
#     # for the current label
#     labelMask = np.zeros(dn2_img.shape, dtype="uint8")
#     labelMask[labels == label] = 255
#     numPixels = cv2.countNonZero(labelMask)
#       # If the number of pixels in the component is between lower bound and upper bound, 
#     # add it to our mask
#     if numPixels > lower and numPixels < upper:
#         mask = cv2.add(mask, labelMask)
#  #mask2=cv2.dilate(mask,(5,5),iterations=2)
# cv2_imshow(mask)

# image=mask.copy()

# if image.shape[0]>image.shape[1]:
#   h=(image.shape[0]-image.shape[1])/2
#   added_image = cv2.copyMakeBorder(image,0,0,int (h),int (h),cv2.BORDER_CONSTANT, None, 0)
# else:
#   h=(image.shape[1]-image.shape[0])/2
#   added_image = cv2.copyMakeBorder(image,int (h),int (h),0,0,cv2.BORDER_CONSTANT, None, 0)

# cv2_imshow(added_image)

# roi=added_image.copy()


# image_f = cv2.copyMakeBorder(roi,int (.1*roi.shape[0]),int (.1*roi.shape[0]),int (.1*roi.shape[1]),int (.1*roi.shape[1]),cv2.BORDER_CONSTANT, None, 0)

# cv2_imshow(image_f)

# model=keras.models.load_model("/content/gdrive/MyDrive/mosaic_2/aryan_folder/all_models3/model.h5")
# model.load_weights("/content/gdrive/MyDrive/mosaic_2/aryan_folder/all_models3/res_chars_weights_baka.hdf5")

# character = cv2.cvtColor(image_f , cv2.COLOR_GRAY2BGR)
# x=cv2.resize(character,(32,32))
# x = np.expand_dims(x, axis=0)
# x.shape
# ans=model.predict(x)
# print(np.argmax(ans))

# !pip install easyocr
# import easyocr

# reader = easyocr.Reader(['en'])

# output = reader.readtext(img)

# output

# predicted_word=pytesseract.image_to_string(img)
# print(predicted_word)

# for img in img2:
#   predict=pytesseract.image_to_string(img,config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 10')
#   print(predict)
#   cv2_imshow(img)

# predicted=pytesseract.image_to_string(img2[2], lang='eng',config='--psm 8')
# for predict in predicted:
#   print(predict)