#include <WiFi.h>
#include <HTTPClient.h>
 
const char* ssid = "YOUR_SSID";
const char* password =  "YOUR_PASSWORD";

int pin_state = 0;

#define LED_PIN 3
 
void setup() {
 
  Serial.begin(115200);
  delay(4000);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
  pinMode(LED_PIN, OUTPUT);
 
}
 
void loop() {
 
  if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection 
status
 
    HTTPClient http;
 
    http.begin("http://167.172.163.38/api/v1/alexa"); //Specify the URL
    int httpCode = http.GET();                                        
//Make the request
 
    if (httpCode > 0) { //Check for the returning code
 
        String payload = http.getString();
        Serial.print("Code -> ");
        Serial.println(httpCode);
        Serial.print("Payload -> ");
        Serial.println(payload);
        Serial.println("");
        pin_state = payload.toInt();

        if (pin_state == 1)
        {
            digitalWrite(LED_PIN, HIGH);
        }
        else if (pin_state == 0)
        {
            digitalWrite(LED_PIN, LOW);
        }

        else
        {
            Serial.println("Wrong pin state!");
        }
        }
 
    else {
      Serial.println("Error on HTTP request");
    }
 
    http.end(); //Free the resources
  }
 
  delay(1000);
 
}
