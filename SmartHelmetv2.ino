#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define BUZZERL 14
void setup () {
 
  Serial.begin(115200);
  WiFi.begin("Montilla Y Rodriguez", "montilla123");
  pinMode(BUZZERL, OUTPUT);
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting..");
 
  }
  Serial.println("Connected to WiFi Network");
 
}
 
void loop() {
 
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    HTTPClient http;  //Declare an object of class HTTPClient
 
    http.begin("http://192.168.1.4:5000/update"); //Specify request destination
 
    int httpCode = http.GET(); //Send the request
 
    if (httpCode > 0) { //Check the returning code
 
      String payload = http.getString();   //Get the request response payload
      double dist = payload.toDouble();
      Serial.println(payload);           //Print the response payload
          
      if(dist < 6 && dist > 3){
        Serial.print("Danger ");
        Serial.println(dist);
        digitalWrite(BUZZERL,HIGH);
        delay(500);
      }
        
     else if(dist < 3){
        Serial.print("Danger ");
        Serial.println(dist);
        digitalWrite(BUZZERL,HIGH);
        delay(1000);
         

    } else {
     digitalWrite(BUZZERL,LOW);

      }

 
    }else Serial.println("An error ocurred");
 
    http.end();   //Close connection
 
  }
 
  delay(10); //Send a request every 10 seconds
 
}
