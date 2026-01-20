import cv2
import numpy as np
import os
import tensorflow as tf  # Using full TF for Mac, TFLite is similar

# ----------------------
# Step 3a: Load model
# ----------------------
MODEL_PATH = "detect.tflite"
LABEL_PATH = "labelmap.txt"

# Load labels
with open(LABEL_PATH, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Input size
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# ----------------------
# Step 3b: Prepare image list
# ----------------------
image_folder = "offline_camera"
images = sorted(os.listdir(image_folder))

# Folder to save cropped dog images
os.makedirs("cropped_dogs", exist_ok=True)

# ----------------------
# Step 3c: Loop over images
# ----------------------
for img_file in images:
    frame = cv2.imread(os.path.join(image_folder, img_file))

    # Resize + normalize
    resized = cv2.resize(frame, (width, height))
    input_data = np.expand_dims(resized, axis=0)
    input_data = np.float32(input_data) / 255.0

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get outputs
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]   # Bounding boxes
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class IDs
    scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence scores

    h, w, _ = frame.shape

    # Loop through detections
    for i in range(len(scores)):
        if scores[i] > 0.6:  # confidence threshold
            class_id = int(classes[i])
            label = labels[class_id]

            if label == "dog":
                ymin, xmin, ymax, xmax = boxes[i]

                # Scale boxes to original image size
                xmin = int(xmin * w)
                xmax = int(xmax * w)
                ymin = int(ymin * h)
                ymax = int(ymax * h)

                # Draw box
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                text = f"{label}: {int(scores[i]*100)}%"
                cv2.putText(frame, text, (xmin, ymin-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                # Save cropped dog
                crop = frame[ymin:ymax, xmin:xmax]
                crop_file = os.path.join("cropped_dogs", f"{img_file}_dog{i}.jpg")
                cv2.imwrite(crop_file, crop)

    # Display image (optional)
    cv2.imshow("Dog Detection Simulation", frame)
    cv2.waitKey(500)  # 500ms per image

cv2.destroyAllWindows()
print("Simulation complete! Cropped dog images saved in 'cropped_dogs/'")
