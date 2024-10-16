/*
  Knock Sensor

  This sketch reads a piezo element to detect a knocking sound.
  It reads an analog pin and compares the result to a set threshold.
  If the result is greater than the threshold, it writes "knock" to the serial
  port, and toggles the LED on pin 13.

  The circuit:
	- positive connection of the piezo attached to analog in 0
	- negative connection of the piezo attached to ground
	- 1 megohm resistor attached from analog in 0 to ground

  created 25 Mar 2007
  by David Cuartielles <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Knock
*/


// these constants won't change:
const int knockSensor = A0;  // the piezo is connected to analog pin 0


// these variables will change:
int sensorReading = 0;  // variable to store the value read from the sensor pin



void setup() {
  Serial.begin(9600);       // use the serial port
  Serial.println("OK");
}

void loop() {
  // read the sensor and store it in the variable sensorReading:
  sensorReading = analogRead(knockSensor);
  Serial.println(sensorReading);
  // if the sensor reading is greater than the threshold:
    if (Serial.available())
    Serial.write(Serial.read());
  delay(100);  // delay to avoid overloading the serial port buffer
}
