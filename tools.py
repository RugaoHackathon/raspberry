
import json
def buildMsg(location):
    msgDict = {}
    msgDict["from"] = "VIDEO"
    msgDict["type"] = "VIDEOINFO"
    msgDict["data"] = location
    return json.dumps(msgDict)



def buildMotorMsg(motorAngle):
    motorMsg = {}
    motorMsg["from"] = "AngleCaculator"
    motorMsg["type"] = "ANGLE"
    motorMsg["data"] = motorMsg

    return json.dumps(motorMsg)