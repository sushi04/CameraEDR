# CAMERA EDR
This repos consists of Event Data Recorder. It records the video data around the event.

## Setup

1. Install Python 3.x if not already installed.
2. Create a Python Virtual Environment
3. Install required python packages using the Requirement.txt file

## EDR.py

### Usage

1. Run the script 'EDR.py'
2. Enter the camera id, rtsp_link. The video saved will have camera id at the end.
3. Edit the `pre_event_duration` , `post_event_duration` and `camera_fps` as per requirement. Pre_event_duration , Post_event_duration are time for which video must be recorded before and after the event respectively.
4. For giving the trigger, press keyboard key `t`. When a trigger is triggered, it will be displayed on video stream.


## Additional Notes

1. Ensure that the rtsp_link is valid.
2. The time duration for which the video must be recorded should be as per norm.
