import pyautogui
import serial

arduino = serial.Serial('COM4', 115200) #Second is your baud rate
width, height = pyautogui.size()

# Exponential moving average parameters
alpha = 0.2
prev_dx, prev_dy = 0, 0

while True:
    data = arduino.readline().decode('utf-8', errors='ignore').strip()
    if data:
        x, y = [float(val) for val in data.split(",")]
        dx = x * 100  # previously 10, increased by a factor of 5
        dy = y * 100  # previously 10, increased by a factor of 5

        # Apply exponential moving average
        dx = alpha * dx + (1 - alpha) * prev_dx
        dy = alpha * dy + (1 - alpha) * prev_dy
        prev_dx, prev_dy = dx, dy

        # Move the cursor
        pyautogui.move(dx, dy)
