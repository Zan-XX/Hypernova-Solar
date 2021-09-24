//Reads data from a DS1620+ temperature sensor and sends it over the CAN bus
//URL for DS1620.h https://github.com/msparks/arduino-ds1620
//URL for SPI.h https://github.com/arduino/ArduinoCore-avr/blob/master/libraries/SPI/src/SPI.h
extern "C"{
  #include "conv.h"
};

#include "mcp_can.hpp"
#include "mcp_can_dfs.h"

#include "DS1620.h"

#include "SPI.h"

static const uint8_t dq = 3;
static const uint8_t clk = 4;
static const uint8_t rst = 5;

MCP_CAN CAN0(10);

DS1620 ds1620(rst, clk, dq);
void setup() {
  //Serial setup
  Serial.begin(115200);
  //DS1620+ setup
  ds1620.config();
  //MCP2515 setup
  if (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.println("MCP2515 Initialized Successfully");
  } else {
    Serial.println("Error Initializing MCP2515...");
  }
  CAN0.setMode(MCP_NORMAL);
}

byte *data;

void loop() {
  int temp_c = ds1620.temp_c() * 10; //Multiply reading by 10 to maintain 1 decimal point of accuracy.
	//Adding support for other data types later
  
  data =  intToByteArr(temp_c);
  
  byte sndStat = CAN0.sendMsgBuf(0x102, 0, int_len, data); //ID: 258, Standard CAN Frame, 2 bytes
  
  if (sndStat == CAN_OK) {
    Serial.println("Message Sent Successfully");
  } else {
    Serial.println("Error Sending Message...");
  }
  
  delay(100);
}
