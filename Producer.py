#coding:utf-8


from MsgClient import MsClient
from config import *
import sys
sys.path.append("/home/pi/SungemSDK/api/")
from FaceDector import FaceDetector
import cv2
from tools import buildMsg
import time

if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)
    #client.start()

    faceDetector = FaceDetector()

    while True:

        result = faceDetector.faceDect()

        key = cv2.waitKey(5000)
        client.senMsg(subscription,result)


        # get face objector
        if len(result[0]) > 0:
            box = result[0]

            if box[5] - box[3] > 10 or box[4] - box[2] > 10:
                faceMsg = buildMsg(result)
                client.senMsg(subscription, faceMsg)