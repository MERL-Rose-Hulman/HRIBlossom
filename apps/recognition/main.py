import mediapipe as mp
import cv2
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizer, GestureRecognizerOptions, GestureRecognizerResult


"""
The default model, gesture_recognizer.task, detects the following gestures:
👍, 👎, ✌️, ☝️, ✊, 👋, 🤟

To create a custom model, we need to train it on our own data.
Using the collect_images_simple.py script, we can collect images of the gestures we want to train on.
The GESTURES constant in top of the file is list of all gestures we want to train. Adding a gesture to the list will add it to the model once the training is complete.

The trained model is saved in the gestures/gesture_model.task file.
To train the model, run the folowing script in your terminal: (requires docker to be installed)
    cd apps/recognition/train && docker build -t gesture-trainer .

    docker run --rm -v "${PWD}/training_data:/workspace/data" -v "${PWD}/models:/workspace/output" gesture-trainer

Note: After running docker run..., the script will appear in the docker desktop app.
"""

CAMERA_INDEX = 0
GESTURE_DICT = {
    "None": "reset",
    "Closed_Fist": "reset",
    "Open_Palm": "reset",
    "Pointing_Up": "reset",
    "Thumb_Down": "reset",
    "Thumb_Up": "reset",
    "Victory": "reset",
    "ILoveYou": "reset",
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

current_gesture = "None"

def handle_gesture_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp: int):
    global current_gesture
    print("Gesture result received")
    try:
        if result.gestures:
            categories = result.gestures
            gesture = categories[-1][-1].category_name
            current_gesture = gesture
            print(f"Gesture: {current_gesture}")
            
            sequence_name = GESTURE_DICT.get(gesture, "reset")
            print(f"Mapped to sequence: {sequence_name}")

            # sequence = get_sequence_by_name(sequence_name)
            # if sequence is None:
            #     print(f"No sequence found for: {sequence_name}")
            #     return

            # sequence.run()
            print(f"Would run sequence: {sequence_name}")
        else:
            current_gesture = "None"
    except Exception as e:
        print(f"Error in gesture callback: {e}")
        current_gesture = "Error"

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='./gestures/gesture_recognizer.task'),
    running_mode=VisionTaskRunningMode.LIVE_STREAM,
    num_hands=1,
    result_callback=handle_gesture_result
  )


def draw_landmarks_on_frame(frame, hand_landmarks):
    """Draw hand landmarks and connections on the frame"""
    if hand_landmarks:
        for hand_landmark in hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmark,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
    return frame


def main():
    with GestureRecognizer.create_from_options(options) as recognizer:
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            vid = cv2.VideoCapture(CAMERA_INDEX)
            timestamp = 0

            if not vid.isOpened():
                print("Error: Could not open camera")
                return

            print("Starting camera feed... Press 'q' to quit")
            
            vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            vid.set(cv2.CAP_PROP_FPS, 30)
            
            frame_count = 0
            
            while True:
                ret, frame = vid.read()
                if not ret:
                    print(f"Error: Failed to capture frame {frame_count}")
                    if frame_count == 0:
                        print("Camera might not be available or accessible")
                    break

                frame_count += 1

                try:
                    frame = cv2.flip(frame, 1)
                    
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    results = hands.process(frame_rgb)
                    
                    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                    
                    if results.multi_hand_landmarks:
                        frame_bgr = draw_landmarks_on_frame(frame_bgr, results.multi_hand_landmarks)
                    
                    cv2.putText(frame_bgr, f"Gesture: {current_gesture}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame_bgr, "Press 'q' to quit", (10, frame_bgr.shape[0] - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    cv2.imshow('Hand Gesture Recognition', frame_bgr)
                    
                    if frame_count % 30 == 0:
                        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                        recognizer.recognize_async(mp_image, timestamp)
                except Exception as e:
                    print(f"Error processing frame {frame_count}: {e}")
                    continue
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quit key pressed")
                    break
 
                timestamp += 1
        
            print("Exiting main loop...")

            vid.release()
            cv2.destroyAllWindows()



if __name__ == "__main__":
    main()