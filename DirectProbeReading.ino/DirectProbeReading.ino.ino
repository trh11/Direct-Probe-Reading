unsigned long deltatime;
unsigned long previousMillis;
int minutes = 15;
int PIN[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};

void setup()  {
  Serial.begin(9600);
  deltatime = minutes*60000;
  previousMillis = 0;
}

void loop(){
  if (millis() - previousMillis >= deltatime-490)
  {
    previousMillis = millis();
    int i;
    for (i = 1; i <= 15; i++)
    {
      float IN[]={analogRead(PIN[i])*5/1023.0};
      Serial.print(IN[i]);
      if (i == 15)
      {
        break;
      }
      Serial.print(",");
    }
    Serial.flush();
  }
}
