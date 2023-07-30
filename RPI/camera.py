import cv2
from picamera2 import Picamera2
import time
piCam = Picamera2()
# configuration for the camera image
piCam.preview_size=(1280,720)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

fps = 0

while True:
    tStart = time.time()
    frame = piCam.capture_array()
    # gives frame rate
    cv2.putText(frame, str(int(fps)), (30,60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255),3)
    # open image shown on camera
    cv2.imshow("piCam", frame)
    # end camera usage
    if cv2.waitKey(1) == ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    # calculate frame rate per second
    fps = .9*fps + .1*1/loopTime
    print(int(fps))
cv2.destroyAllWindows()
