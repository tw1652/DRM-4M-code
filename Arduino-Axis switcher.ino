#include <DHT.h>
#include <DHT_U.h>

#define DHTPin 8
#define DHTTYPE DHT22

float readingX;
float readingY;
float readingZ;
float humidity = -1;
float temperature = -300;
const int led=13;
int value =4;

DHT dht(DHTPin, DHTTYPE);

void setup(){
  Serial.begin(9600);
  dht.begin();
  pinMode(2, OUTPUT); //X1
  pinMode(4, OUTPUT);//Y1
  pinMode(6, OUTPUT);//Z1
/*
  //X
  digitalWrite (2, LOW);
  //Y
  digitalWrite (4, LOW);
  // Z
  digitalWrite (6, LOW);
*/
}

void loop() 
{ 
  while (Serial.available()>0){
    value = Serial.parseInt();
    delay(50);
  }
  if (value == 0){
    X_axis();
  } else if (value == 1){
    Y_axis();
  } else if(value == 2){
    Z_axis();
  } else if(value == 3){
    Temp();
  }
}

void X_axis() {
  digitalWrite (2, LOW);
  digitalWrite (4, LOW);
  digitalWrite (6, LOW);
}
void Y_axis() {
  digitalWrite (2, LOW);
  digitalWrite (4, LOW);
  digitalWrite (6, HIGH);
}
void Z_axis(){
  digitalWrite (2, HIGH);
  digitalWrite (4, LOW);
  digitalWrite (6, LOW);
}
void Temp(){
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  Serial.print(humidity);
  Serial.println(" %");
  Serial.print(temperature);
  Serial.println(" °C");

}