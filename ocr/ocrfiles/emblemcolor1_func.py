import cv2
import numpy as np
import warnings
import urllib.request

#Ignore Deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)


#defining a function to detect the 'color1' template
def emblemcolor1(image):
    if(image.split('.')[-1]) != 'jpg':
        img = cv2.imread(image)
        success,buffer = cv2.imencode(".jpg",img)
        img = cv2.imdecode(buffer,cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(image)
        
    #print(img.shape)
    #Scale the image size
    if (img.shape[0]<=900):
        scale_percent = 85
        #scale_percent = 80
        #scale_percent = 75

    elif (img.shape[0]<=1000):
        #scale_percent = 60
        scale_percent = 75

    elif (img.shape[0]<=2000):
        #scale_percent = 50
        scale_percent = 55

    elif (img.shape[0]<=3000):
        #scale_percent = 30
        scale_percent = 45

    elif(img.shape[0]>3000):
        #scale_percent = 22
        scale_percent = 35
    else:
        pass

    #scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 112.5)
    height = int(img.shape[0] * scale_percent / 112.5)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    # Convert it to grayscale
    img_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)


    #Read the templates
    url_emblem = "https://i.ibb.co/dGBw3gJ/Emblem.jpg"
    url_color = "https://i.ibb.co/KGfRtzW/color1.jpg"
    
    with urllib.request.urlopen(url_emblem) as emb :
            e = emb.read()
    img_emb = np.array(bytearray(e),dtype=np.uint8)
    img_emb = cv2.imdecode(img_emb,cv2.IMREAD_COLOR)
    img_emb = cv2.cvtColor(img_emb,cv2.COLOR_BGR2GRAY)

    with urllib.request.urlopen(url_color) as col :
            f = col.read()
    img_color = np.array(bytearray(f),dtype=np.uint8)
    img_color = cv2.imdecode(img_color,cv2.IMREAD_COLOR)
    img_color = cv2.cvtColor(img_color,cv2.COLOR_BGR2GRAY)
    
    template1 = img_emb
    
    template2 = img_color

    #Store width and height of template in w and h
    w1, h1 = template1.shape[::-1]
    w2, h2 = template2.shape[::-1]

    try :
        res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
        res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
    except:
        template2 = cv2.resize(template2,(800,650))
        res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
        res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)


    
    threshold_list_emblem = [0.80,0.78,0.76,0.74,0.72,0.70,0.68,0.66]
    threshold_list_color1 = [0.80,0.78,0.76,0.74,0.72,0.70,0.68,0.66]
    ## Store the coordinates of matched area in an array and draw a rectangle around the region
    for threshold1 in threshold_list_emblem:
        loc1 = np.where( res1 >= threshold1)
        #loc2 = np.where( res2 >= threshold)

        for pt in zip(*loc1[::-1]):
            draw1 = cv2.rectangle(resized, pt, (pt[0] + w1, pt[1] + h1), (0,255,255), 2)
            #draw2 = cv2.rectangle(resized, pt, (pt[0] + w2, pt[1] + h2), (0,255,255), 2)
        try:
            if draw1 !=[]:
                break
        except:
            pass
    for threshold2 in threshold_list_color1:
        #loc1 = np.where( res1 >= threshold2)
        loc2 = np.where( res2 >= threshold2)

        for pt2 in zip(*loc2[::-1]):
            draw2 = cv2.rectangle(resized, pt2, (pt2[0] + w2, pt2[1] + h2), (0,255,255), 2)
        try:

            if draw2 !=[]:
                break
        except:
            pass
    try:
       try:
           if draw1!=[]:
                  return 1
       except:
           pass
       try:
           if draw2!=[]:
                  return 1
       except:
           pass
       return 0
    except:
       return 0
if __name__ == "__main__":

    ## Local testing purposes
    img = "abhf.jpg"

    print(emblemcolor1(img))
