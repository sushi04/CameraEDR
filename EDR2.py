import cv2
import time
from collections import deque
import os
import queue
import threading
from datetime import datetime
import logging

q=queue.Queue()
    
def Receive(rtsp_link):
    global cap
    global ret
    print("starting to receive")
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = "video_codec"
    cap = cv2.VideoCapture(rtsp_link)
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)
    return frame


def record_event():

    pre_event_duration=30
    post_event_duration=10
    camera_id=2
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = "video_codec"

    #cap = cv2.VideoCapture('rtsp://192.168.1.15:8554/h264') 
    
    frame = q.get()

    filename = f"video_recording_{camera_id}.mp4"
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capfps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width, frame_height))

    pre_event_buffer = deque(maxlen=pre_event_duration * 30)  
    triggered = False

    while cap.isOpened():
        frame = q.get()
        if ret:
            if not triggered:
                cv2.putText(frame, 'Normal Operation', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Event Triggered', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', frame)
        
            if cv2.waitKey(1) & 0xFF == ord('t'):
                triggered = True
                start_time = time.time()
                #trigger_time = datetime.now()


            if not triggered:
                if len(pre_event_buffer) < pre_event_duration * 30:
                    pre_event_buffer.append(frame)
                else:
                    out.write(pre_event_buffer.pop()) 
            else:

                if time.time() - start_time >= post_event_duration:
                    break
                else:
                  out.write(frame)  
                
                
        else:
            break

        #if trigger_time is not None:
             #logging.info("Trigger Time: %s", trigger_time)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def Videostream(rtsp_link):
    p1=threading.Thread(target=Receive, args = (rtsp_link,))
    p3 = threading.Thread(target=record_event)
    p1.start()
    p3.start()
    p3.join()

i=1
for i in range(1,1000):
  Videostream('rtsp://192.168.1.15:8554/h264')
  continue

