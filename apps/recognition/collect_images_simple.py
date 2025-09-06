#!/usr/bin/env python3
"""
Simple image collection for MediaPipe training.
"""

import cv2
import time
from pathlib import Path

CAMERA_INDEX = 0
DATA_DIR = "./training_data"
GESTURES = ["thumbs_up", "peace_sign", "closed_fist", "open_palm", "none"]

def main():
    for gesture in GESTURES:
        Path(DATA_DIR, gesture).mkdir(parents=True, exist_ok=True)
    
    current_gesture = 0
    
    vid = cv2.VideoCapture(CAMERA_INDEX)
    
    print(f"Collecting images for: {GESTURES[current_gesture]}")
    print("SPACE: Save image, N: Next gesture, Q: Quit")
    
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        
        # Show current gesture
        cv2.putText(frame, f"Gesture: {GESTURES[current_gesture]}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Collect Images', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            # Save image
            timestamp = int(time.time() * 1000)
            filename = f"{DATA_DIR}/{GESTURES[current_gesture]}/{GESTURES[current_gesture]}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
            
        elif key == ord('n'):
            # Next gesture
            current_gesture = (current_gesture + 1) % len(GESTURES)
            print(f"Switched to: {GESTURES[current_gesture]}")
            
        elif key == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
