#include <LiquidCrystal.h>
LiquidCrystal lcd(12,11,5,4,3,2);
int val;
int tempPin = 1;

void setup() {
  lcd.begin (16,2);
}

void loop() {
  val = analogRead(tempPin);
  lcd.print("TEMPURATURE = ");
  lcd.setCursor(0,1);
  lcd.print(val);
  lcd.setCursor(5,1);
  lcd.print(" *C");
  delay(1000);
  lcd.clear();
}
