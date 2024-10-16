import subprocess
import serial
import time

THRESHOLD = 75.0  
SKETCH = "sketch_oct14b/sketch_oct14b.ino"
PORT = "/dev/cu.usbmodem11301"


def compileArduino(SKETCH):
    try:
        compileCommand = f"arduino-cli compile --fqbn arduino:avr:uno {SKETCH}"
        subprocess.run(compileCommand, check=True, shell=True)
        print("Compilation successful!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")

def uploadArduino(SKETCH, port):
    try:
        uploadCommand = f"arduino-cli upload -p {port} --fqbn arduino:avr:uno {SKETCH}"
        subprocess.run(uploadCommand, check=True, shell=True)
        print("Upload successful!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during upload: {e}")

def sendThresholdToArduino(port, threshold):
    arduino = serial.Serial(port, 9600, timeout=1)
    time.sleep(10)
    arduino.write( f'{str(threshold)}\n'.encode())
    arduino.close()

compileArduino(SKETCH)
uploadArduino(SKETCH, PORT)
sendThresholdToArduino(PORT, THRESHOLD)

