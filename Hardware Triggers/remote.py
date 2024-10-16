import subprocess
import serial
import time

new_threshold = 75.0  
sketchPath = "sketch_oct14b/sketch_oct14b.ino"

def compileArduino(sketchPath):
    try:
        compileCommand = f"arduino-cli compile --fqbn arduino:avr:uno {sketchPath}"
        subprocess.run(compileCommand, check=True, shell=True)
        print("Compilation successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")

def uploadArduino(sketchPath, port):
    try:
        uploadCommand = f"arduino-cli upload -p {port} --fqbn arduino:avr:uno {sketchPath}"
        subprocess.run(uploadCommand, check=True, shell=True)
        print("Upload successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error during upload: {e}")

def sendThresholdToArduino(port, threshold):
    arduino = serial.Serial(port, 9600, timeout=1)
    
    time.sleep(10)
    
    threshold_str = str(threshold) + "\n"  # Add newline to mark end of input
    arduino.write(threshold_str.encode())
    arduino.close()
arduinoPort = "/dev/cu.usbmodem11301"

compileArduino(sketchPath)
uploadArduino(sketchPath, arduinoPort)
sendThresholdToArduino(arduinoPort, new_threshold)

