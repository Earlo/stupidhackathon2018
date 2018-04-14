import numpy as np
import cv2

from teppo import Tulppu


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def draw_teppos(img, teppoes, thickness = 1):
    for key in teppoes:
        x, y, w, h = teppoes[key].box
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), teppoes[key].getCol(), thickness)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,str(key),(x,y), font, 1,(255,0,255),2,cv2.LINE_AA)


def checkIfOldTeppo(teppoes, tep):
    best = [-1, 0.0]
    for key in teppoes:
        v = teppoes[key].isAlike(tep)
        if v > best[1]:
            best = [key, v]

    if ((best[1] > 0.8) and (best[0] != -1)):
        #The teppo seeems to be one from before
        teppoes[best[0]].update(*tep)
        return True
    else:
        #a new teppo is here
        #if for ValueError
        print(len(teppoes), teppoes.items() )
        if (len(teppoes) > 0):
            teppoes[max(teppoes.keys())+1] = Tulppu(*tep)
        else:
            teppoes[0] = Tulppu(*tep)
        return False

if __name__ == '__main__':
    teppoes = {}

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    #try:
    #    cap=cv2.VideoCapture(1)
    #except:
    cap=cv2.VideoCapture(0)
    cv2.useOptimized()
    while True:
        _,frame=cap.read()
        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        
        for t in found:
            len(teppoes)
            if ((t[2] > 0) and (t[3] > 0)):
                
                print(checkIfOldTeppo(teppoes,t))
        #draw_detections(frame,found)
        draw_teppos(frame, teppoes)
        ded = []
        for key in teppoes:
            teppoes[key].grow()
            if (teppoes[key].isDead()):
                ded.append(key)
        for d in ded:
            teppoes.pop(d, None)

        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

    cv2.destroyAllWindows()
