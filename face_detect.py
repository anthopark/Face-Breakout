"""This is face_dect.py

It helps load face detectors and detect face from the camera frame.
Existing code(wrtten by Adrian Rosebrock, author of pyimagesearch.com) is repurposed 
"""

import argparse
import cv2
from imutils.video import VideoStream
import imutils
import numpy


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


def getDNN():
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    return net


def getCamFrame(videoStream):
    camFrame = videoStream.read()
    camFrame = imutils.resize(camFrame, width=800, height=600)
    cv2.flip(camFrame, 1, camFrame)
    return camFrame


def getFaceXCoord(camFrame, net):
    (h, w) = camFrame.shape[0:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(camFrame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence < args["confidence"]:
            continue

        box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        return startX + abs(endX - startX) // 2
