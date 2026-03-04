import cv2
import RPi.GPIO as GPIO
import numpy as np
import time

# GPIO Pins Configuration
TRIG       = 23   # Ultrasonic Trigger Pin
ECHO       = 24   # Ultrasonic Echo Pin
RELAY      = 17   # Relay Control Pin
BUZZER     = 27   # Buzzer Pin
GAS_SENSOR = 22   # Gas Sensor Pin (MQ-3)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,       GPIO.OUT)
GPIO.setup(ECHO,       GPIO.IN)
GPIO.setup(RELAY,      GPIO.OUT)
GPIO.setup(BUZZER,     GPIO.OUT)
GPIO.setup(GAS_SENSOR, GPIO.IN)   # Gas Sensor as Input

# Default State
GPIO.output(RELAY,  GPIO.HIGH)    # Relay ON initially
GPIO.output(BUZZER, GPIO.LOW)     # Buzzer OFF initially

def get_distance():
    """Measure distance using Ultrasonic Sensor"""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)            # 10us pulse
    GPIO.output(TRIG, False)

    timeout    = time.time() + 1   # 1-second timeout
    start_time = None
    end_time   = None

    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            return 999             # Timeout error
        start_time = time.time()

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            return 999             # Timeout error
        end_time = time.time()

    if start_time is None or end_time is None:
        return 999                 # Handle case where no valid reading is received

    elapsed_time = end_time - start_time
    distance     = (elapsed_time * 34300) / 2   # Convert to cm
    return round(distance, 2)

def detect_color(img):
    """Detect Red and White Colors in Camera Feed"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define Red Color Range
    lower_red1 = np.array([0,   120,  70])
    upper_red1 = np.array([10,  255, 255])
    lower_red2 = np.array([170, 120,  70])
    upper_red2 = np.array([180, 255, 255])

    # Define White Color Range
    lower_white = np.array([0,   0, 200])
    upper_white = np.array([180, 30, 255])

    # Create Color Masks
    mask_red1  = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2  = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red   = mask_red1 + mask_red2
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    red_pixels   = cv2.countNonZero(mask_red)
    white_pixels = cv2.countNonZero(mask_white)

    is_red_detected   = red_pixels   > 500
    is_white_detected = white_pixels > 500

    return is_red_detected, is_white_detected

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)   # Initialize Camera
    cap.set(3, 640)             # Set Width
    cap.set(4, 480)             # Set Height

    try:
        while True:
            distance     = get_distance()
            gas_detected = GPIO.input(GAS_SENSOR)   # Check Gas
            print(f"Distance: {distance} cm")

            success, img = cap.read()
            if not success:
                continue

            is_red_detected, is_white_detected = detect_color(img)

            # Logic: If Distance < 15cm OR Red Color Detected OR Gas NOT Detected -> Relay OFF, Buzzer ON
            if distance < 15 or is_red_detected or not gas_detected:
                GPIO.output(RELAY,  GPIO.LOW)    # Relay OFF
                GPIO.output(BUZZER, GPIO.HIGH)   # Buzzer ON

                if is_red_detected:
                    print("Red Signal Detected -> Relay OFF")
                elif is_white_detected:
                    print("Ambulance Detected -> Relay OFF")
                elif not gas_detected:
                    print("Alcohol Detected -> Relay OFF, Buzzer ON")
            else:
                GPIO.output(RELAY,  GPIO.HIGH)   # Relay ON
                GPIO.output(BUZZER, GPIO.LOW)    # Buzzer OFF
                print("Safe Condition -> Relay ON")

            # Display on Video Feed
            cv2.putText(img, f"Distance: {distance} cm",
                        (50, 50),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if not gas_detected:
                cv2.putText(img, "Alcohol Detected",
                            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Live Video", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):   # Press 'q' to exit
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
