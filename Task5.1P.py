import serial
from datetime import datetime
import firebase_admin
from firebase_admin import db


databaseURL = 'https://task-5-1p-default-rtdb.asia-southeast1.firebasedatabase.app/'
cred_obj = firebase_admin.credentials.Certificate(
    'task-5-1p-firebase-adminsdk-xo741-ab9db6588c.json'
)
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL
	})

ref = db.reference("/")

# CREATE INITIAL DATABASE

data = {  

	"Accelerometer":
	{

    },
}

ref.set(data)


# set baud rate, same speed as set in your Arduino sketch.
boud_rate = 300

# set serial port as suits your operating system
s = serial.Serial('COM9', boud_rate)

# Read from serial port. 
read = s.readline().decode("utf-8").strip()

while True:  # infinite loop, keep running

    # Read from serial port. 
    read = s.readline().decode("utf-8").strip()
    
    if read:
        data = read.split(", ") # Splits the data with a ","
        print(data)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Reads the current time in a specific format
        ref.child('Accelerometer').child(timestamp).child("X").set(data[0])
        ref.child('Accelerometer').child(timestamp).child("Y").set(data[1])
        ref.child('Accelerometer').child(timestamp).child("Z").set(data[2])

