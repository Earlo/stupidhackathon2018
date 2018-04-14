import numpy as np
import cv2

from teppo import Tulppu


class VideoCamera(object):
    def __init__(self, index):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(index)
        self.video.set(3,480)
        self.video.set(4,640)

        self.teppoes = {}

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.recognition()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()



    def recognition(self):
        _,frame=self.video.read()
        found,w=self.hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        
        for t in found:
            self.checkIfOldTeppo(t)
        self.draw_teppos(frame)

        ded = []
        for key in self.teppoes:
            self.teppoes[key].grow()
            if (self.teppoes[key].isDead()):
                ded.append(key)
        for d in ded:
            self.teppoes.pop(d, None)

        return frame


    def draw_teppos(self, img, thickness = 1):
        for key in self.teppoes:
            x, y, w, h = self.teppoes[key].box
            # the HOG detector returns slightly larger rectangles than the real objects.
            # so we slightly shrink the rectangles to get a nicer output.
            pad_w, pad_h = int(0.15*w), int(0.05*h)
            cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), self.teppoes[key].getCol(), thickness)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,str(key),(x,y), font, 1,(255,0,255),2,cv2.LINE_AA)


    def checkIfOldTeppo(self, tep):
        best = [-1, 0.0]
        for key in self.teppoes:
            v = self.teppoes[key].isAlike(tep)
            if v > best[1]:
                best = [key, v]

        if ((best[1] > 0.8) and (best[0] != -1)):
            #The teppo seeems to be one from before
            self.teppoes[best[0]].update(*tep)
            return True
        else:
            #a new teppo is here
            #if for ValueError
            if (len(self.teppoes) > 0):
                self.teppoes[max(self.teppoes.keys())+1] = Tulppu(*tep)
            else:
                self.teppoes[0] = Tulppu(*tep)
            return False

