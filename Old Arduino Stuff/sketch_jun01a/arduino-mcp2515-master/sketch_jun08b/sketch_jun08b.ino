#include <SPI.h>

#include "mcp2515.h"

const int spiCSPin = 10;

int ledHIGH    = 1;

int ledLOW     = 0;



MCP2515 CAN(spiCSPin);



void setup()

{

    Serial.begin(115200);



    while (CAN_OK != CAN.begin(CAN_500KBPS))

    {

        Serial.println("CAN BUS init Failed");

        delay(100);

    }

    Serial.println("CAN BUS Shield Init OK!");

}



unsigned char stmp[8] = {ledHIGH, 1, 2, 3, ledLOW, 5, 6, 7};

    

void loop()

{   

  Serial.println("In loop");

  CAN.sendMsgBuf(0x43, 0, 8, stmp);

  delay(1000);

}
