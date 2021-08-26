#include <SPI.h>

#include "mcp_can.h"



const int spiCSPin = 10;

const int ledPin = 2;

boolean ledON = 1;



MCP_CAN CAN(spiCSPin);



void setup()

{

    Serial.begin(115200);

    pinMode(ledPin,OUTPUT);



    while (CAN_OK != CAN.begin(CAN_500KBPS))

    {

        Serial.println("CAN BUS Init Failed");

        delay(100);

    }

    Serial.println("CAN BUS  Init OK!");

}





void loop()

{

    unsigned char len = 0;

    unsigned char buf[8];



    if(CAN_MSGAVAIL == CAN.checkReceive())

    {

        CAN.readMsgBuf(&len, buf);



        unsigned long canId = CAN.getCanId();



        Serial.println("-----------------------------");

        Serial.print("Data from ID: 0x");

        Serial.println(canId, HEX);



        for(int i = 0; i<len; i++)

        {

            Serial.print(buf[i]);

            Serial.print("\t");

            if(ledON && i==0)

            {



                digitalWrite(ledPin, buf[i]);

                ledON = 0;

                delay(500);

            }

            else if((!(ledON)) && i==4)

            {



                digitalWrite(ledPin, buf[i]);

                ledON = 1;

            }

        }

        Serial.println();

    }

}
