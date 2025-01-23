import os
import cv2


#Selecting region of interest:
#Draw the rectange -> Press space to confirm it -> Repeat steps
#Press space without any rectangles to move onto the next image
#If you do not like the rectangle draw, you can simply draw a new one and it will delete the unwanted rectange (The rectangle cannot be confirmed)


def generate_negative_desc_file(): #Creates neg.txt which stores the location of your negative images.
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

def save_coordinates(image_name, rects): #Saves location of your positive imagees as well as where the traffic cone appears in said images and how many times it appears.
    num_rects = len(rects)
    with open("pos.txt", "a") as file:
        rects_str = '  '.join([f"{x} {y} {w} {h}" for (x, y, w, h) in rects])
        file.write(f"positive/{image_name}  {num_rects}  {rects_str}\n")

def main(image_folder):
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path)
        rectangles = []

        while True:
            temp_image = image.copy()
            for rect in rectangles:
                cv2.rectangle(temp_image, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (255, 0, 0), 2)
            
            cv2.imshow("Image", temp_image)
            rect = cv2.selectROI("Image", temp_image, fromCenter=False)

            if rect[2] == 0 or rect[3] == 0:  # If width or height is zero, stop selecting. So just press space without selecting any rectangles.
                break
            
            rectangles.append(rect)
            

        if rectangles:  # It will only saves if there are rectangles
            save_coordinates(image_name, rectangles)

        cv2.destroyAllWindows()

if __name__ == "__main__":
    main("/Users/pratheeksunilkumar/TrafficConeDetection/.venv/positive")