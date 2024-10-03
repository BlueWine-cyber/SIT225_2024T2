#include <DHT.h>
#include <Servo.h>

// Define constants
const int DHT_PIN = 2;
const int SERVO_PIN1 = 5;
const int SERVO_PIN2 = 6;

// Initialize DHT sensor and servos
DHT dht(DHT_PIN, DHT11);
Servo servo1;
Servo servo2;

// Initialize variables
float humidity = 0.0;
float temperature = 0.0;
float effectiveTemperature = 0.0;
int angle = 0;
unsigned long lastReadTime = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  servo1.attach(SERVO_PIN1);
  servo2.attach(SERVO_PIN2);
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastReadTime > 1000) {
    // Read humidity and temperature
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    effectiveTemperature = temperature - 0.4 * (temperature - 10) * (1.0 - (humidity / 100));

    // Print readings to serial monitor
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print(" %\t");
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" *C\t");
    Serial.print("Effective Temperature: ");
    Serial.print(effectiveTemperature);
    Serial.println(" *C");

    lastReadTime = currentTime;
  }

  // Check for errors
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Error reading");
    return;
  }

  // Control servos based on effective temperature
  if (effectiveTemperature < 26) {
    servo1.write(95);
    delay(300);
    servo2.write(120);
  } else if (effectiveTemperature > 28) {
    servo1.write(0);
    delay(200);
    servo2.write(118);
  }
}
