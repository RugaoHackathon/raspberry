#coding:utf-8


from MsgClient import MsClient
from config import *

END_STRING = "finish"
import json
from duojidd import duojidd
def processMessage(msg):
    message = json.loads(msg.decode("utf8"))

    if message['from'] =='AngleCaculator' and message['type']=='MOTOCTL':

        degreeInfo = None
        try:
            degreeInfo = message['data']
        except Exception as e:
            print(e)
        degreeX = degreeInfo['degreeX']
        degreeZ = degreeInfo['degreeZ']
        duojidd(degreeX,degreeZ)

    try:
        if message['from'] =='ALICLOUD' and message['type']=='MOTOCTL':
            degreeInfo = None
        try:
            degreeInfo = message['data']
        except Exception as e:
            print(e)
        degreeX = degreeInfo['degreeX']
        degreeZ = degreeInfo['degreeZ']
        duojidd(degreeX,degreeZ)
        
    except Exception as e:
        print(e)
        
        
    
    
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
            print("message")
            print(message)
     
            processMessage(message)
