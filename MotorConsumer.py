#coding:utf-8


#coding:utf-8


from MsgClient import MsClient
from config import *

END_STRING = "finish"
import json
from duojidd import duojidd
def processMessage(msg):
    message = json.loads(msg.decode("utf8"))
<<<<<<< HEAD
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
        
        
    
    

=======
    try:
        if message['from'] =='AngleCaculator' and message['type']=='SETANGLE':

            degreeInfo = None
            try:
                degreeInfo = message['data']
            except Exception as e:
                print(e)
            degreeX = degreeInfo['degreeX']
            degreeZ = degreeInfo['degreeZ']
            duojidd(degreeX,degreeZ)
    except Exception, e:
        print(e)
        pass
>>>>>>> 32536a7c04c2136204e5c62dfd4df7a100202772

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
            print('item')
            print(item)
            message = item['data']
            print("message")
            print(message)
     
            processMessage(message)
