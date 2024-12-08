from ultralytics import YOLO
import cv2
import os

import pandas as pd  

# Define folder paths and model path
folderPath = "C://Users//ength//Desktop//29th Projects//ASU Manufacturing Program//MFG598 Python//Projecct Work//FinalPokerCardsDetection4Video//PokerCardFrames//Round"
modelPath = "C://Users//ength//Desktop//29th Projects//ASU Manufacturing Program//MFG598 Python//Projecct Work//FinalPokerCardsDetection4Video//googlecolab//weights//weights//best.pt"
ExcelPath = "C://Users//ength//Desktop//29th Projects//ASU Manufacturing Program//MFG598 Python//Projecct Work//FinalPokerCardsDetection4Video//PokerCardDataset//PokerCardCalculator//Results.xlsx"

def processingImages(folderPath, modelPath):
    model = YOLO(modelPath) #Again we have to load the yolo model for processing each image!! 
    print(f"Model loaded from: {modelPath}")

    # Check if the folder exists
    if not os.path.exists(folderPath):
        print(f"Error: Folder '{folderPath}' does not exist.")
        return

    # Get list of image files in the folder
    imageFiles = sorted([f for f in os.listdir(folderPath) if f.endswith(".jpg")])

    if not imageFiles:
        print(f"Th Round Folder is empty!! Something wrong, check please: {folderPath}")
        return

    print(f"Processing {len(imageFiles)} images from folder: {folderPath}")

    all_detections = []  # Store all detections across images

    for imagefile in imageFiles:
        imagePath = os.path.join(folderPath, imagefile)
        img = cv2.imread(imagePath)

        if img is None:
            print(f"Failuare: {imageFiles}")
            continue

        # Yolo model!!! 
        results = model.predict(img, conf=0.1)  
        # Adjust confidence threshold if you have bad lighting or the cam focus is not accurate!! 

        # Extract detections and bounding boxes
        detections = []
        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0].tolist())  
            label_index = int(result.cls[0].item())  
            confidence = float(result.conf[0].item())  
            label = f"{model.names[label_index]}"
            detections.append({
                "image_file": imagefile,
                "label": label,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "confidence": confidence
            })

        # I wanna Add all detections to the final list to look at in the terminal
        all_detections.extend(detections)

        # Draw bounding boxes and labels on the image
        for det in detections:
            x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, det["label"], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the image with detections
        cv2.imshow("Detections", img)
        key = cv2.waitKey(1000)  # Display each image for 1 second (adjust as needed)
        # Press 'q' to exit early
        if key == ord('Q'):  
            break

    cv2.destroyAllWindows()

    # Print summary of all detections
    print("\nAll Detections:")
    for det in all_detections:
        print(f" - {det['label']} at ({det['x1']}, {det['y1']}, {det['x2']}, {det['y2']}) (Confidence: {det['confidence']:.2f})")

    # Here I have a few issues and I needed to add extention "try"
    try:
        df = pd.DataFrame(all_detections)
        df.to_excel(ExcelPath, index=False)
        print(f"great, Results are ready and saved to Excel file: {ExcelPath}")
    except Exception as e:
        print(f" Excel can not be saved!! : {e}")

if __name__ == "__main__":
    processingImages(folderPath, modelPath)
