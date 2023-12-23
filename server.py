# server.py

from flask import Flask, render_template, Response, request, session, redirect, url_for
import app
import secrets
import config

flask_app = Flask(__name__)
flask_app.secret_key = secrets.token_hex(16)

@flask_app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('not_logged_in.html')
    return render_template('index.html')

@flask_app.route('/video_feed')
def video_feed():
    return Response(app.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@flask_app.route('/login', methods=['GET', 'POST'])
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

@flask_app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.start_camera_thread()
    app.start_record_thread()
    
    try:
        flask_app.run(host='0.0.0.0', port=12971)
    except Exception as e:
        print("Error running Flask app:", e)
    finally:
        app.stop_recording()
