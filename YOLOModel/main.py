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

    # Resize to 640x480 (You can go smaller for faster processing).
    frame_resized = cv2.resize(frame, (640, 480))

    # Get current time for FPS
    new_frame_time = time.time()

    results = model(frame_resized, conf=0.3) #This applies the model  

    largestConeCoordinates = []
    largestArea = 0

    if results and results[0].boxes is not None:
        for result in results:
            xyxys = result.boxes.xyxy #xyxy is in the format: (x_min, y_min, x_max, y_max)
            for xyxy in xyxys:
                smallx = xyxy[0].item()
                smally = xyxy[1].item()
                largex = xyxy[2].item()
                largey = xyxy[3].item()
                print(f"Small x: {smallx}")
                print(f"Large y: {largey}")
                print(f"Large x: {largex}")
                print(f"Small y: {smally}")
                
                areaofCone = 0.5 * (largex - smallx) * (largey - smally)
                print(f"Area of Cone: {areaofCone}")
                print(f"Largest area: {largestArea}")
                if areaofCone > largestArea:
                    print("Entered loop!")
                    largestArea = areaofCone
                    largestConeCoordinates = [smallx, smally, largex, largey]
                    print("Appending data...")
                    

    print(f"{largestConeCoordinates}, {largestArea}")
    if largestConeCoordinates:
        center_x = (largestConeCoordinates[0] + largestConeCoordinates[2]) / 2 
        frame_center_x = 640 / 2  
        print("Entered loop!")

        if center_x < frame_center_x:
            print("The drone should turn right\n")
        else:
            print("The drone should turn left\n")

        
    
    
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
