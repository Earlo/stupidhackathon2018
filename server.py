from flask import Flask, render_template, Response, request
from camera import VideoCamera
import threading
import time

app = Flask(__name__)

camera1 = VideoCamera(0)
camera2 = VideoCamera(1)
cameras = [camera1, camera2]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    try:
        e = int(request.args.get('Eye'))
        w = int(request.args.get('Who'))
        cameras[e].toggleTeppo(w)
    except IndexError:
        pass

    return render_template('admin.html')


def gen1():
    while True:
        frame = camera1.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0)


def gen2():
    while True:
        frame = camera2.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0)



def loop1(func):
    while True:
        func()


def loop2(func):
    while True:
        func()


@app.route('/left_video_feed')
def left_video_feed():
    threading.Thread(target=gen1, args=()).start()
    return Response(gen1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/right_video_feed')
def right_video_feed():
    threading.Thread(target=gen2, args=()).start()
    return Response(gen2(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
