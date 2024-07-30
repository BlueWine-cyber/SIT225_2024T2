import serial
import csv
from datetime import datetime

# set baud rate, same speed as set in your Arduino sketch.
boud_rate = 300

# set serial port as suits your operating system
s = serial.Serial('COM9', boud_rate)

with open ("Arduino.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "X", "Y", "Z"])

    while True:  # infinite loop, keep running

        # Read from serial port. 
        read = s.readline().decode("utf-8").strip()
        
        if read:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Reads the current time in a specific format
            data = read.split(", ") # Splits the data with a ","
            writer.writerow([timestamp] + data) # Writes data into csv
