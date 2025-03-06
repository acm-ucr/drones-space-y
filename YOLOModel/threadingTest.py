from ultralytics import YOLO
import cv2
import time
import queue
import threading

model = YOLO("best.pt") 
cap = cv2.VideoCapture(0)

frameQ = queue.Queue()  # .put() and .get()
resultsQ = queue.Queue()
largeCordQ = queue.Queue()
largeAreaQ = queue.Queue()

# Use threading.Event for synchronized control of threads
stop_event = threading.Event()

def frameCapture(cap, stop_event):
    count = 5
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            stop_event.set()  # Stop all threads if capture fails
            return
        frame_resized = cv2.resize(frame, (640, 480))
        count -= 1
        if count == 0:
            frameQ.put(frame_resized)
            count = 5

def modelThread(stop_event):
    while not stop_event.is_set():
        if frameQ.empty():
            time.sleep(0.01)
            continue
        frame_resized = frameQ.get()
        results = model(frame_resized, conf=0.35)
        largestConeCoordinates = []
        largestArea = 0
        resultsQ.put(results)
        largeCordQ.put(largestConeCoordinates)
        largeAreaQ.put(largestArea)

def proccessCoords(stop_event):
    while not stop_event.is_set():
        if resultsQ.empty():
            time.sleep(0.01)
            continue
        results = resultsQ.get()
        largestConeCoordinates = largeCordQ.get()
        largestArea = largeAreaQ.get()

        if results and results[0].boxes is not None:
            for result in results:
                xyxys = result.boxes.xyxy
                for xyxy in xyxys:
                    smallx = xyxy[0].item()
                    smally = xyxy[1].item()
                    largex = xyxy[2].item()
                    largey = xyxy[3].item()
                    areaofCone = 0.5 * (largex - smallx) * (largey - smally)
                    if areaofCone > largestArea:
                        largestArea = areaofCone
                        largestConeCoordinates = [smallx, smally, largex, largey]
                        
        if largestConeCoordinates:
            center_x = (largestConeCoordinates[0] + largestConeCoordinates[2]) / 2 
            frame_center_x = 640 / 2
            if center_x < frame_center_x:
                print("The drone should turn right\n")
            else:
                print("The drone should turn left\n")

        annotated_frame = results[0].plot()
        cv2.imshow('Webcam Feed', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()  # Stop threads when 'q' is pressed

# Create threads
capture_thread = threading.Thread(target=frameCapture, args=(cap, stop_event))
capture_thread.start()

model_thread = threading.Thread(target=modelThread, args=(stop_event,))
model_thread.start()

process_thread = threading.Thread(target=proccessCoords, args=(stop_event,))
process_thread.start()

# Wait for threads to finish
capture_thread.join()
model_thread.join()
process_thread.join()

cap.release()
cv2.destroyAllWindows()
