import serial
import random
import time
import datetime

# set baud rate, same speed as set in your Arduino sketch.
boud_rate = 9600

# set serial port as suits your operating system
s = serial.Serial('COM7', boud_rate, timeout=5)


while True:  # infinite loop, keep running

    #  a random number between 1 and 5.
    random_time = random.randint(1, 5)

    # Timestamp
    timestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    
    # Sends number to arduino
    d = s.write(bytes(str(random_time), 'utf-8'))
    print(timestamp)
    print(f" Send >>> {random_time} ({d} bytes)")

    time.sleep(d+0.5) # Delay before sending the next step

    # Receives number from arduino
    slp = s.readline().decode("utf-8")
    slpresponse = int(float(slp))

    timestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    print(timestamp)
    print(f" Recv <<< {slpresponse}")

    print("sleep: ", slpresponse)

    time.sleep(slpresponse)
    
