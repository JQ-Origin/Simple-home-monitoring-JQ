# app.py

import cv2
import threading
import datetime
from queue import Queue
import time
import config

camera_lock = threading.Lock()
frame_queue = Queue(maxsize=10)
is_recording = True
camera = cv2.VideoCapture(0)

# 设置摄像头的分辨率
camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_RESOLUTION[0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_RESOLUTION[1])

out = None

last_frame_time = 0
frame_counter = 0
fps = 0

def get_video_writer():
    now = datetime.datetime.now()
    filename = config.VIDEO_SAVE_PATH + now.strftime("%Y-%m-%d") + ".avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(filename, fourcc, 20.0, config.CAMERA_RESOLUTION)

def put_timestamp_and_framerate(frame, fps):
    font = cv2.FONT_HERSHEY_SIMPLEX
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, 30), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"{fps:.2f} FPS", (frame.shape[1] - 100, 30), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    return frame

def calculate_fps():
    global last_frame_time, frame_counter, fps
    current_time = time.time()
    if last_frame_time != 0:
        time_diff = current_time - last_frame_time
        instant_fps = 1 / time_diff if time_diff > 0 else 0
        fps = (fps * frame_counter + instant_fps) / (frame_counter + 1)
        frame_counter += 1
    last_frame_time = current_time
    return fps

def capture_frames():
    global camera, last_frame_time
    while True:
        with camera_lock:
            success, frame = camera.read()
            if not success:
                break
            calculate_fps()  # 更新实时帧率
            frame_queue.put(frame)

def record_video():
    global is_recording, out
    last_date = datetime.datetime.now().date()
    while is_recording:
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame_with_timestamp = put_timestamp_and_framerate(frame, fps)
            out.write(frame_with_timestamp)
            current_date = datetime.datetime.now().date()
            if current_date > last_date:
                out.release()
                out = get_video_writer()
                last_date = current_date

def gen_frames():
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame_with_timestamp = put_timestamp_and_framerate(frame, fps)
            ret, buffer = cv2.imencode('.jpg', frame_with_timestamp)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def start_camera_thread():
    threading.Thread(target=capture_frames, daemon=True).start()

def start_record_thread():
    global is_recording, out
    out = get_video_writer()
    threading.Thread(target=record_video, daemon=True).start()

def stop_recording():
    global is_recording, camera, out
    is_recording = False
    with camera_lock:
        camera.release()
    if out is not None:
        out.release()
