import io,os
import json
import cv2
import numpy as np
import requests

def ocr(image):
    if(image.split('.')[-1]) != 'jpg':
        img = cv2.imread(image)
        success,buffer = cv2.imencode(".jpg",img)
        img = cv2.imdecode(buffer,cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(image)
    #print(f'Dimensions of the image : {img.shape}')
    img_size = os.stat(image).st_size
    #print(img_size)
    if (img_size>=1000000):

        if (img.shape[0]<=850):
            #scale_percent = 75
            scale_percent = 77

        elif (img.shape[0]<=1000):
            #scale_percent = 60
            scale_percent = 62

        elif (img.shape[0]<=2000):
            #scale_percent = 50
            scale_percent = 52

        elif (img.shape[0]<=3000):
            #scale_percent = 30
            scale_percent = 32

        elif(img.shape[0]>3000):
            #scale_percent = 22
            scale_percent = 29
        else:
            pass

        #scale_percent = 60 # percent of original size
        width = int(img.shape[1] * scale_percent / 112.5)
        height = int(img.shape[0] * scale_percent / 112.5)
        dim = (width, height)

        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img = resized
    else:
        pass

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])

    file_bytes = io.BytesIO(compressedimage)
    
    # YOUR_API_KEY =  Insert Your api key
    result = requests.post(url_api,
                  files = {image: file_bytes},
                  data = {"apikey": "YOUR_API_KEY", 
                          "language": "eng"})

    result = result.content.decode()
    result = json.loads(result)
    #print(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    #print(text_detected)


    return text_detected
