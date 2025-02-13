from ultralytics import YOLO
import cv2
import time


model = YOLO("best.pt") 


cap = cv2.VideoCapture(0)


frame_rate = 60 # Target FPS
prev_frame_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize to 640x480 or smaller for faster processing
    frame_resized = cv2.resize(frame, (640, 480))

    # Get current time for FPS
    new_frame_time = time.time()

    results = model(frame_resized) #This applies the model  

    
    annotated_frame = results[0].plot()  

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Display FPS
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the results
    cv2.imshow('Webcam Feed', annotated_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
