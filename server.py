from flask import Flask, render_template, Response
from camera import VideoCamera1, VideoCamera2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/left_video_feed')
def left_video_feed():
    return Response(gen(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/right_video_feed')
def right_video_feed():
    return Response(gen(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)