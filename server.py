from flask import Flask, render_template, Response
from camera import VideoCamera1, VideoCamera2, ImageGetter, JoinedImage
from multiprocessing import Process
import time
import numpy as np

app = Flask(__name__)
left_frames = ""
right_frames = ""

@app.route('/')
def index():
    return render_template('index.html')


def timed_left(t):
    gen1(VideoCamera1)
    time.sleep(t)

def timed_right(t):
    gen2(VideoCamera2)
    time.sleep(t)

def gen1(camera):
    global left_frames
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0)

def gen2(camera):
    global right_frames
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0)


@app.route('/video_feed')
def video_feed():
    return Response(JoinedImage(VideoCamera1(), VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/left_video_feed')
def left_video_feed():
    #async_response = Process(target=gen1, args=(VideoCamera1(),)).start()
    return Response(ImageGetter(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/right_video_feed')
def right_video_feed():
    #async_response = Process(target=gen2, args=(VideoCamera2(),)).start()
    return Response(ImageGetter(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
