from ultralytics import YOLO
import cv2
import threading
import time


model = YOLO("best.pt") 

frame = None
annotated_frame = None
largestConeCoordinates = []
largestArea = 0
areaofCone = 0


def vidCap():
    global frame, largestConeCoordinates
    cap = cv2.VideoCapture(0)
    print("5")
    while True:
        ret, new_frame = cap.read()
        if ret:
            with threading.Lock():
                frame = new_frame
        time.sleep(0.03)
    

def applyModel():
    print("6")
    global frame
    global largestArea
    global largestConeCoordinates
    global annotated_frame
    while True:
        with threading.Lock():
            if frame is not None:
                frame_resized = cv2.resize(frame, (640, 480))
                results = model(frame_resized, conf=0.35)
                largestConeCoordinates.clear()
                largestArea = 0
                if results and results[0].boxes is not None:
                    for result in results:
                        xyxys = result.boxes.xyxy #xyxy is in the format: (x_min, y_min, x_max, y_max)
                        for xyxy in xyxys:
                            smallx = xyxy[0].item()
                            smally = xyxy[1].item()
                            largex = xyxy[2].item()
                            largey = xyxy[3].item()
                            
                            areaofCone = 0.5 * (largex - smallx) * (largey - smally)
                            if areaofCone > largestArea:
                                largestArea = areaofCone
                                largestConeCoordinates = [smallx, smally, largex, largey]

                    print(f"{largestConeCoordinates}, {largestArea}")
                    if largestConeCoordinates:
                        center_x = (largestConeCoordinates[0] + largestConeCoordinates[2]) / 2 
                        frame_center_x = 640 / 2  

                        if center_x < frame_center_x:
                            print("The drone should turn right\n")
                        else:
                            print("The drone should turn left\n")
                    annotated_frame = results[0].plot()


def show_frame():
    global annotated_frame
    while True:
        with threading.Lock():
            if annotated_frame is not None:
                cv2.imshow('Webcam Feed', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




def main():

    print("1")
    thread1 = threading.Thread(target=vidCap, daemon=True)
    print("2")
    thread2 = threading.Thread(target=applyModel, daemon=True)
    print("3")
    thread1.start()
    print('4')
    thread2.start()

    show_frame()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()