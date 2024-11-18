import subprocess
import serial
import time
from datetime import datetime  # Import datetime for timestamps
import csv

THRESHOLD = 65.0  
SKETCH = "HardwareTriggers/sketch_oct14b/sketch_oct14b.ino"
PORT = "/dev/cu.usbmodem11401"
CSV_FILE = "HardwareTriggers/dht_readings.csv"

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

def logSerialData(port, csv_file):
    print("Connecting to Arduino...")
    arduino = serial.Serial(port, 9600, timeout=1)
    time.sleep(2)
    with open(csv_file, mode = 'a') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Date_Time','Temperature', 'Humidity'])
        print("Logging data to csv. Press Ctrl+C to stop logging.")
        try:
            while True:
                line = arduino.readline().decode('utf-8').strip()
                if line.startswith('Humidity:'):
                    print(line)

                    try:
                        parts = line.split(',')
                        humidity = float(parts[0].split(":")[1].strip()[:-1])
                        temperature = float(parts[1].split(":")[1].strip().split()[0])
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([timestamp, temperature, humidity])
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing data: {e}")
        except KeyboardInterrupt:
            print("Logging stopped.")
            arduino.close()
        finally:
            arduino.close()


compileArduino(SKETCH)
uploadArduino(SKETCH, PORT)
sendThresholdToArduino(PORT, THRESHOLD)
logSerialData(PORT, CSV_FILE)

