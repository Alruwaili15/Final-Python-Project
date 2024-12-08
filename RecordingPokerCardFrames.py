import cv2
import os
import time
# The main idea of this code to save the cards in frames 
# to make it easy on the Yolo model to detect as pics! 
# I create a folder called Round! 
def createFolder(path, name="Round"):
    Round  = os.path.join(path,name)
    counter = 1

    # If the folder Round already saved this step to save the new one with numbering the folders! 
    while os.path.exists(Round):
        Round = os.path.join(path, f"{name}{counter}")
        counter += 1

    os.makedirs(Round)
    print(f"Folder created: {Round}")
    return Round

def captureFrames(path, duration=100): # here is how long the recording gonna be! 
    folder_path = createFolder(path)

    
    cap = cv2.VideoCapture(1) 
    if not cap.isOpened():
        print("There is an Error: The cam does not run!!!!")
        return

    print(f"Capturing frames for {duration} seconds")
    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Something wrong with the frame! check!!")
            break

        # here, I need to Save each frame as an image in the Round folder! 
        frame_filename = os.path.join(folder_path, f"frame_{frame_count:04d}.jpg")
        if cv2.imwrite(frame_filename, frame):
            print(f"Saved frame {frame_count} to {frame_filename}")
        else:
            print(f"Frame is Not saved!!!  {frame_count}")
        frame_count += 1

        # Stop it after the desired time! 
        if time.time() - start_time > duration:
            break

    # turn on the camera
    cap.release()
    print(f"Saved {frame_count} frames to folder: {folder_path}")
    # Specify the base path for saving frames!! 
if __name__ == "__main__":
    
    base_path = "C://Users//ength//Desktop//29th Projects//ASU Manufacturing Program//MFG598 Python//Projecct Work//FinalPokerCardsDetection4Video//PokerCardFrames"
    captureFrames(base_path, duration=30)
