#coding:utf-8


from MsgClient import MsClient
from config import *
import sys
sys.path.append("/home/pi/SungemSDK/api/")

from FaceDetector import FaceDetector
import cv2
from tools import buildMsg
import time

import numpy as np
import base64
from PIL import Image
from io import BytesIO
import requests

# def request(imgData):
#     url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
#     payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"api_key\"\r\n\r\nNAn44x2m6ME5pU1SV4KNOCQnhleMwS9y\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"api_secret\"\r\n\r\n48tVTbhSiPBhEtwwJ09YGAMWySN0GwAV\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image_base64\"\r\n\r\n"+imgData+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"return_attributes\"\r\n\r\nemotion\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
#     headers = {
#         'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
#         'Cache-Control': "no-cache",
#         'Postman-Token': "60d8c2c8-6d96-4dea-98c3-a2414b8ccdd3"
#     }
#     response = requests.request("POST", url, data=payload, headers=headers)
#     print(response.text)
#     return response.text

# def emotion(img):
#     pil_img = Image.fromarray(img)
#     buff = BytesIO()
#     pil_img.save(buff, format="JPEG")
#     new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
#     return request(new_image_string)

if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)
    #client.start()

    faceDetector = FaceDetector()

    while True:

        result = faceDetector.faceDect()
        image = result[0]
        bbs = result[1]
        key = time.sleep(3)

        boundingBoxes = []
        for i in bbs:
            print(i)
            i[1] = str(i[1])
            boundingBoxes.append(i)

        imageInfo = {}
        imageInfo['imageShape'] = image.shape
        if len(boundingBoxes)==0:
            boundingBoxes = []

        imageInfo['bbs'] = boundingBoxes
        faceMsg = buildMsg(imageInfo)
        print(faceMsg)
        client.senMsg(subscription,faceMsg)

        #print(emotion(image))

