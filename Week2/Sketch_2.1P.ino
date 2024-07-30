#include <Arduino_LSM6DS3.h> //includes the accelerometer module

void setup() {
  // put your setup code here, to run once:
  Serial.begin(300); //set baud rate
  while(!Serial) //waits for open port

  if (!IMU.begin()) { 
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  //Prints LSM6DS3's sample rate 
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());

}

void loop() {
  // put your main code here, to run repeatedly:

  if (IMU.accelerationAvailable()) {
    float x, y, z;
    IMU.readAcceleration(x, y, z);

    Serial.print(x, 3); 
    Serial.print(", ");
    Serial.print(y, 3);
    Serial.print(", ");
    Serial.println(z, 3);

  }
}
