#!/bin/bash

nohup python3 MotorConsumer.py 2>&1 >> motor.log &

nohup python3 PersonPostionConsumer.py 2>&1 >> person.log &

nohup python3 FaceDetectorProducer.py 2>&1 >> facedector.log &

