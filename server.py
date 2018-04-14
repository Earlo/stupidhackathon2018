from flask import Flask, render_template, Response
from camera import VideoCamera1, VideoCamera2
from multiprocessing import Process
import time

app = Flask(__name__)
left_frames = ""
right_frames = ""

@app.route('/')
def index():
    return render_template('index.html')


def gen1(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0)

def gen2(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0)

@app.route('/left_video_feed')
def left_video_feed():
    async_response = Process(target=gen1, args=(VideoCamera1(),)).start()
    return Response(async_response.get(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/right_video_feed')
def right_video_feed():
    async_response = Process(target=gen2, args=(VideoCamera2(),)).start()
    return Response(async_response.get(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
