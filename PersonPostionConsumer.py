#coding:utf-8


from MsgClient import MsClient
from config import *

from FaceDector import FaceDetector
import cv2
from tools import buildMsg,buildMotorMsg
import math

import json



END_STRING = "finish"

import time

hasPerson = False

XANGLE = 0
YANGLE = 0

startXAngle = -30
startYAngle = -15

count = 0

IMAGEWIDTH = 1800
IMAGEHEIGTH = 1600

CARWIDTH = 180

MAXCOUNT = 20

PERX = 0
PERY = 0
PERZ = 0



def isFace(faceInfo):
    if len(faceInfo[0]) > 0:
        box = faceInfo[0]
        score = box[1]
        if box[5] - box[3] > 10 or box[4] - box[2] > 10 and score > 0.55:
            return True

    return False

def getXangle(imageLocation,widthSize,angle):
    score = imageLocation[1]
    x1 = imageLocation[2]
    y1 = imageLocation[3]
    x2 = imageLocation[4]
    y2 = imageLocation[5]
    if score > 0.55:
        xMiddle = (x1+x2)/2
        if xMiddle>(widthSize/2-50) and xMiddle<(widthSize/2+50):
            return angle

    return None


def getYangle(imageLocation, heightSize, angle):
    score = imageLocation[1]
    x1 = imageLocation[2]
    y1 = imageLocation[3]
    x2 = imageLocation[4]
    y2 = imageLocation[5]
    if score > 0.55:
        yMiddle = (y1 + y2) / 2
        if yMiddle > (heightSize / 2 - 20) and yMiddle < (heightSize / 2 + 20):
            return angle

    return None

def getPosition(xAngle,yAngle,carWidth):
    assert(xAngle>-90 and xAngle<90)
    assert (yAngle>-90 and yAngle<90)
    x = float(carWidth)/4
    y = (float(carWidth)/4)/math.tan(abs(xAngle))
    z = y*math.tan(abs(yAngle))
    return (x,y,z)


def getBestAngle(x,y,z):

    xAngle = -10
    yAngle = -5
    return (xAngle,yAngle)

def processMessage(message,client,subscription):
    global XANGLE
    global YANGLE
    global hasPerson
    global  count

    #步进 度数
    step = 2

    if message['from'] in ('VIDEO',):
        if message['type'] in ('VIDEOINFO',):
            faceInfo = message['data']

            #检测到有人
            if isFace(faceInfo):

                if not hasPerson and (count < MAXCOUNT):
                    count =count+1

                #检测到有人进来 开始计算 最佳位置
                if not hasPerson and count> MAXCOUNT:
                    hasPerson = True
                    #移动到初始位置
                    xAdd = XANGLE - startXAngle
                    yAdd = YANGLE - startYAngle
                    XANGLE = startXAngle
                    YANGLE = startYAngle

                    motorAngle = {
                        'xAngle': xAdd,
                        'yAngle': yAdd
                    }
                    msg = buildMotorMsg(motorAngle)
                    client.senMsg(subscription,msg)
                    time.sleep(1)

                if hasPerson:
                    xAngle = getXangle(faceInfo,IMAGEWIDTH,XANGLE)
                    if not xAngle:
                        xAdd = step
                        XANGLE = XANGLE + xAdd
                        yAdd = 0
                        YANGLE = YANGLE+yAdd
                        motorAngle = {
                            'xAngle': xAdd,
                            'yAngle': yAdd
                        }
                        msg = buildMotorMsg(motorAngle)
                        client.senMsg(subscription, msg)
                        time.sleep(1)

                    yAngle = getYangle(faceInfo,IMAGEHEIGTH,YANGLE)
                    if not yAngle:

                        xAdd = 0
                        XANGLE = XANGLE + xAdd
                        yAdd = step
                        YANGLE = YANGLE + yAdd

                        motorAngle = {
                            'xAngle': xAdd,
                            'yAngle': yAdd
                        }
                        msg = buildMotorMsg(motorAngle)
                        client.senMsg(subscription, msg)
                        time.sleep(1)
                    if xAngle and yAngle:

                        x,y,z = getPosition(xAngle,yAngle,CARWIDTH)
                        print(x,y,z)
                        bestXangle,bestYangle = getBestAngle(x,y,z)
                        xAdd = XANGLE - bestXangle
                        yAdd = YANGLE - bestYangle
                        XANGLE = bestXangle
                        YANGLE = bestYangle

                        motorAngle = {
                            'xAngle': xAdd,
                            'yAngle': yAdd
                        }
                        msg = buildMotorMsg(motorAngle)
                        client.senMsg(subscription, msg)
                        time.sleep(1)


            else:
                # 没有人
                if hasPerson and count>0:
                    count=count-1
                else:
                    count = 0
                    hasPerson = False



if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)

    while True:
        for item in client.pubsub.listen():
            if item['type'] in ("subscribe", "unsubscribe"):
                continue
            if str(item['data'], 'utf-8') in (END_STRING,):
                client.pubsub.unsubscribe()
                break
            message = item['data']
            print(message)
            message = json.loads(message)

            processMessage(message,client,subscription)
            print(XANGLE,YANGLE)