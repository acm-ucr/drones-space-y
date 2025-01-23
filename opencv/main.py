import numpy as np
import cv2

#Code template was taken from: https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html

traffic_cone_cascade = cv2.CascadeClassifier('cascade/cascade.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cones = traffic_cone_cascade.detectMultiScale(gray, minSize = (24, 24), scaleFactor=1.1, minNeighbors=8)

    for (x,y,w,h) in cones:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
    cv2.imshow('img',img)
    if cv2.waitKey(1) == ord('q'):
        print("Closing window...")
        print()
        break

cap.release()

cv2.destroyAllWindows()


#Command to train the model: opencv_traincascade -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 1000 -numNeg 2000 -numStages 10 -maxFalseAlarmRate 0.3 -minHitRate 0.999 
#I found these values to be good.
#Make sure that the NEG count acceptance Ratio does exceed more than 4 zeros after decimal place.