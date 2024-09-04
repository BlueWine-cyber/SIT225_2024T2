#include "thingProperties.h"

const int trigger = 8;
const int echo = 7;

int getUltrasonicDistance(){
  // Function to retreive the distance reading of the ultrasonic sensor
  long duration;
  float distance;

  // Assure the trigger pin is LOW:
  digitalWrite(trigger, LOW);
  // Brief pause:
  delayMicroseconds(5);

  // Trigger the sensor by setting the trigger to HIGH:
  digitalWrite(trigger, HIGH);
  // Wait a moment before turning off the trigger:
  delayMicroseconds(10);
  // Turn off the trigger:
  digitalWrite(trigger, LOW);

  // Read the echo pin:
  duration = pulseIn(echo, HIGH);
  // Calculate the distance in centimeter (CM):
  distance = duration * 0.034 / 2;

  // Return the distance read from the sensor:
  return distance;
}

bool getSensor(){
  // Create variable for sensor
  sensor = false;
  
  if(distance < 10){
    sensor = true;
    Serial.print("Sensor: ");
    Serial.println(sensor);
  }

  else if(distance >= 10) {
    sensor = false;
    Serial.print("Sensor: ");
    Serial.println(sensor);
  }

  // Return the distance read from the sensor:
  return sensor;
}

void setup() {
  // Define inputs and outputs:
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);

  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
 */
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

}

void loop() {
  ArduinoCloud.update();

  // Print the distance to the serial monitor:
  distance = getUltrasonicDistance();
  Serial.print("Distance: ");
  Serial.println(distance);

  // Prints sensor status to serial monitor
  sensor = getSensor();

  // Wait one second before continuing:
  delay(1000);
  
}

void onDistanceChange()  {
  // Add your code here to act upon Distance change
  Serial.println("--onDistanceChange");
}

void onSensorChange()  {
  // Add your code here to act upon Sensor change
  Serial.println("--onSensorChange");
}
