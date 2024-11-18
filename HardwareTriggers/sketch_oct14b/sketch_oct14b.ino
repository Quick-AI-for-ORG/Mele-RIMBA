#include <DHT.h>

#define DHTPIN 12       
#define DHTTYPE DHT22  
#define LED_PIN 13     

DHT dht(DHTPIN, DHTTYPE);

float hum;                
float temp;               
float humidityThreshold = 60.0; 
float temphum;
void setup() {
  Serial.begin(9600);    
  dht.begin();           
  pinMode(LED_PIN, OUTPUT); 
}

void loop() {
  
  if (Serial.available() > 0) {
    
    temphum = Serial.parseFloat(); 
    if(temphum > 0) {
      humidityThreshold = temphum; 
    }
    Serial.print("New humidity threshold set: ");
    Serial.println(humidityThreshold);
  }

  delay(2000);

  
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  if (isnan(hum) || isnan(temp)) {
    Serial.println("Error: Failed to read from DHT sensor!");
    digitalWrite(LED_PIN, LOW); 
  } else {
    
    Serial.print("Humidity: ");
    Serial.print(hum);
    Serial.print(" %, Temp: ");
    Serial.print(temp);
    Serial.println(" Celsius");
    
    
    if (hum > humidityThreshold) {
      digitalWrite(LED_PIN, HIGH); 
    } else {
      digitalWrite(LED_PIN, LOW);  
    }
  }

  delay(300000);  
}