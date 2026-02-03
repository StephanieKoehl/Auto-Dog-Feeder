import cv2
import numpy as np
import tensorflow as tf

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

height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
input_dtype = input_details[0]['dtype']

print("Camera model input:", width, "x", height)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera not accessible")
    exit()

print("Camera started. Press Q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize for model
    resized = cv2.resize(rgb, (width, height))

    # Prepare input
    if input_dtype == np.uint8:
        input_data = np.uint8(resized)
    else:
        input_data = np.float32(resized) / 255.0

    input_data = np.expand_dims(input_data, axis=0)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    h, w, _ = frame.shape

    # Draw detections
    for i in range(len(scores)):
        if scores[i] > 0.4:
            class_id = int(classes[i])
            label = labels[class_id] if class_id < len(labels) else "unknown"
            confidence = scores[i]

            ymin, xmin, ymax, xmax = boxes[i]
            xmin = int(xmin * w)
            xmax = int(xmax * w)
            ymin = int(ymin * h)
            ymax = int(ymax * h)

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            text = f"{label} {int(confidence*100)}%"
            cv2.putText(frame, text, (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Live Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera closed.")
