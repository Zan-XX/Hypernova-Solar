#include <Adafruit_NeoPixel.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//------------------Configuration-------------------

// Device Config
#define TEMP_PIN 8
#define LED_PIN 9
#define LED_COUNT 300

// Temperature Range (F)
#define MAX_TEMP 100
#define MIN_TEMP 30

//--------------------------------------------------

// Define Neopixel strip
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

// Define Temperature sensor bus
OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

// Keep track of sensors on bus
DeviceAddress devAddr[10];
int deviceCount;

void displayTemp(float temp, int index) {

  // Calculate mix of red and blue
  int c = constrain(map((int)temp, MIN_TEMP, MAX_TEMP, 0, 255), 0, 255);
  
  // Change chunk of LEDs depending on index
  strip.fill(strip.Color(c, 0, (255 - c)), (index * 5), 5);
}

void setup() {

  // Initialization
  Serial.begin(9600);
  strip.begin();
  sensors.begin();

  // Request device count from OneWire bus
  deviceCount = sensors.getDeviceCount();

  // Search OneWire bus
  for (int i = 0; i < deviceCount; i++) {
    if (sensors.getAddress(devAddr[i], i)) {

      Serial.print("Found device ");
      Serial.print(i, DEC);
      Serial.print(" with address ");

      for (uint8_t j = 0; j < 8; j++) {
        if (devAddr[i][j] < 16)
          Serial.print("0");
        Serial.print(devAddr[i][j], HEX);
      }

      Serial.println();
    }
    else {

      Serial.print("Found ghost device at ");
      Serial.print(i, DEC);
      Serial.print(" but could not detect address. Check power and cabling");
    }
  }
}

void loop()
{
  // Clear LED strip
  strip.clear();

  // Request temperature update from sensors
  sensors.requestTemperatures();

  // For each sensor
  for (int i = 0; i < deviceCount; i++)
  {
    // Print temperature to serial
    float temp = sensors.getTempF(devAddr[i]);
    Serial.print("Device ");
    Serial.print(i, DEC);
    Serial.print(": ");
    Serial.println(temp);

    // Update corresponding lights
    displayTemp(temp, i);
  }

  // Update lights
  strip.show();

  delay(4000);
}