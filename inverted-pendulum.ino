#include <Arduino.h>

// Hardware setup for Arduino Motor Shield Rev 3
#define DIR_PIN 12
#define SPEED_PIN 3
#define BRAKE_PIN 9
#define CURFB_PIN 0

void setup() {
    Serial.begin(115200);
    pinMode(DIR_PIN, OUTPUT);
    pinMode(SPEED_PIN, OUTPUT);
    pinMode(BRAKE_PIN, OUTPUT);
    pinMode(CURFB_PIN, INPUT);
}

void loop() {
}
