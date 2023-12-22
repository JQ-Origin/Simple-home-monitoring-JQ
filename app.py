from flask import Flask, render_template, Response, request, session, redirect, url_for
import cv2
import threading
import datetime
import secrets
import config  # 导入配置

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 初始化摄像头
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_RESOLUTION[0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_RESOLUTION[1])

def get_video_writer():
    now = datetime.datetime.now()
    filename = config.VIDEO_SAVE_PATH + now.strftime("%Y-%m-%d") + ".avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(filename, fourcc, 20.0, config.CAMERA_RESOLUTION)

out = get_video_writer()

is_recording = True

def record_video():
    global is_recording, camera, out
    last_date = datetime.datetime.now().date()
    while is_recording:
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        current_date = datetime.datetime.now().date()
        if current_date > last_date:
            out.release()
            out = get_video_writer()
            last_date = current_date

threading.Thread(target=record_video).start()

def gen_frames():
    global camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('not_logged_in.html')
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == config.USERNAME and password == config.PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='无效的用户名或密码')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))  # 重定向到登录页面

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=12971)
    finally:
        is_recording = False
        camera.release()
        out.release()
