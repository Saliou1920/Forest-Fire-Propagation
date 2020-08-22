import numpy
import cv2

#change the video directory
cap = cv2.VideoCapture('/Users/salioudiop/Documents/segmentation/video/BW2.mp4')
i = 0
while(cap.isOpened()):
	ret, frame = cap.read()
	if ret == False:
		break
	cv2.imwrite('image'+str(i)+'.png', frame)
	i+= 1

cap.release()
cv2.destroyAllWindows()
