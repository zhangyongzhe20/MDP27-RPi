from picamera import PiCamera
from picamera.array import PiRGBArray

for i in range(0,3):
	with PiCamera() as camera:
	    with PiRGBArray(camera) as stream:
		camera.resolution = (640, 480)
		camera.capture(stream, format='bgr', use_video_port=True) 
		# At this point the image is available as stream.array
		image = stream.array


	ts = time.time()
	oName = str(int(ts)) + ".jpg"
	path = '/home/pi/MDP27-RPi/imageRecognition/testing_images'
	cv2.imwrite(os.path.join(path, oName), image)
