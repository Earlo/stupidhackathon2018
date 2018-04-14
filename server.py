from flask import Flask, render_template, Response
from camera import VideoCamera1, VideoCamera2
from multiprocessing import Process
import numpy as np
import time

app = Flask(__name__)
left_frames = ""
right_frames = ""

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera1, camera2):
    while True:
        frame = np.concatenate((camera1.get_frame(), camera2.get_frame()), axis=0).tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/left_video_feed')
def left_video_feed():
    return Response(gen(VideoCamera1(),VideoCamera2()),
            mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/right_video_feed')
def right_video_feed():
    return Response(gen(VideoCamera1(), VideoCamera2()),
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
