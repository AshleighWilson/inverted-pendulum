#include <Arduino.h>

/* Libs for AS5600 magnetic rotary encoder. */
#include <Wire.h>
#include <AS5600.h>

AMS_5600 ams5600;

// Hardware setup for Arduino Motor Shield Rev 3
#define DIR_PIN 12
#define SPEED_PIN 3
#define BRAKE_PIN 9
#define CURFB_PIN 0

unsigned long startTime;
unsigned long currentTime;

void setup() {
    Serial.begin(115200);
    pinMode(DIR_PIN, OUTPUT);
    pinMode(SPEED_PIN, OUTPUT);
    pinMode(BRAKE_PIN, OUTPUT);
    pinMode(CURFB_PIN, INPUT);

    Wire.begin();
    Serial.println(">>>>>>>>>>>>>>>>>>>>>>>>>>> ");

    if(ams5600.detectMagnet() == 0 ) {
        while(1) {
            if(ams5600.detectMagnet() == 1 ) {
                Serial.print("Current Magnitude: ");
                Serial.println(ams5600.getMagnitude());
                break;
            }
            else {
                Serial.println("Can not detect magnet");
            }
            delay(1000);
        }
    }
    Serial.println("Calibrating pendulum.. ");
    calibrate_pendulum();

    startTime = millis();
    Serial.println("RDY");
}

void loop() {
    /* Raw data reports 0 - 4095 segments, which is 0.087 of a degree. */
    float angle = ams5600.getRawAngle() * 0.087;
    float scaled_angle = (ams5600.getScaledAngle() * 0.087) - 180;

    /* Send the current time and the angle via serial. */
    currentTime = millis() - startTime;
    Serial.println((String) currentTime + " " + scaled_angle);
    delay(10);
}

void calibrate_pendulum() {
    ams5600.setStartPosition(-1);
    ams5600.setEndPosition(-1);
}
