from ultralytics import YOLO
import cv2
import time


model = YOLO("best.pt") 


cap = cv2.VideoCapture(0)


frame_rate = 60 # Target FPS
prev_frame_time = 0

largestConeCoordinates = []
largestArea = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize to 640x480 (You can go smaller for faster processing).
    frame_resized = cv2.resize(frame, (640, 480))

    # Get current time for FPS
    new_frame_time = time.time()

    results = model(frame_resized) #This applies the model  
    if results:
        for result in results:
            xyxys = result.boxes.xyxy
            for xyxy in xyxys:
                smallx = xyxy[0]
                largey = xyxy[1]
                largex = xyxy[2]
                smally = xyxy[3]
                areaofCone = (0.5 * (largex - smallx) * (largey - smally))
                if (not largestConeCoordinates):
                    largestArea = areaofCone
                    largestConeCoordinates.append(smallx)
                    largestConeCoordinates.append(smally)
                    largestConeCoordinates.append(largex)
                    largestConeCoordinates.append(largey)

                else:
                    if areaofCone > largestArea:
                        largestArea = areaofCone
                        largestConeCoordinates[0] = smallx
                        largestConeCoordinates[1] = smally
                        largestConeCoordinates[2] = largex
                        largestConeCoordinates[3] = largey
                if (largestConeCoordinates):
                    if (largestConeCoordinates[0] < (640 / 3)):
                        print(f"The drone should turn right")
                        print()
                        print()
                    elif (largestConeCoordinates[0] > (640 / 3)):
                        print(f"The drone should turn left")
                        print()
                        print()
                    else:
                        print("The drone is in the center. Turn right or left!")
                        print()
                        print()
                largestConeCoordinates.clear()
                
            # xywhs = result.boxes.xywh
            # for xywh in xywhs:
            #     print(xywh)
            #     listofxywh.append(xywh)
    # break
    
    annotated_frame = results[0].plot()

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    

    # Display the FPS
    # cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the results
    cv2.imshow('Webcam Feed', annotated_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Press Q. Abt to close...")
        # print(f"Here is the first element of list of bounding box: {largestConeCoordinates[0]}")
        break


cap.release()
cv2.destroyAllWindows()
