#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <esp_now.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <SPI.h>
#include <OSCMessage.h>

#define DEBUGMODE false;

//Board/Pins
int piezo_pin = A2;

double timestamp;
double piezo;

//Network
WiFiUDP udp;
char *address = "/modeling";
OSCMessage msg(address);

const char* ssid = "EAE";
const char* pword = "";
const char* host = "192.168.50.197"; 
const unsigned port = 8000;


// Initialize both accelerometer and gyroscope components of the IMU
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);

void setup(void) {
  Serial.begin(115200);

  // Connects ESP to network
  
  WiFi.mode(WIFI_STA);
  Serial.print("\nWifi_status: "); 
  WiFi.begin(ssid);
  // Waits while connecting
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("_");
  }

  udp.begin(4000);
  
  //Displays network ssid upon connecting
  Serial.println("");
  Serial.println(WiFi.SSID());

  
  /* Wait for the Serial Monitor */
  while (!Serial) {
    delay(1);
  }

  // Sets up IMU
  Serial.println("Gyroscope Test");
  Serial.println("");

  /* Initialise the sensor */
  if (!gyro.begin()) {
    Serial.println("Ooops, no FXAS21002C detected ... Check your wiring!");
    while (1)
      ;
  }

  // Sets gyro readings to max range of 2000 degrees per second
  gyro.setRange(GYRO_RANGE_2000DPS);
  gyro.setODR(GYRO_ODR_800HZ);

  Serial.println("Accelerometer Test");
  Serial.println("");

  /* Initialise the sensor */
  if (!accelmag.begin()) {
    Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
    while (1)
      ;
  }
  
  // Sets accel readings to max range of 8g
  accelmag.setAccelRange(ACCEL_RANGE_8G);
  accelmag.setSensorMode(ACCEL_ONLY_MODE);
  accelmag.setOutputDataRate(ODR_800HZ);
}


void loop(void) {

  // creates and reads data from imu
  sensors_event_t accelmag_event;
  accelmag.getEvent(&accelmag_event);
  sensors_event_t gyro_event;
  gyro.getEvent(&gyro_event);

  // writes imu data to struct
  timestamp = (micros() / 1000.0);
  piezo = analogRead(piezo_pin);

  if (piezo > 250) {
    sendData(accelmag_event.acceleration.x,
            accelmag_event.acceleration.y,
            accelmag_event.acceleration.z,
            gyro_event.gyro.x,
            gyro_event.gyro.y,
            gyro_event.gyro.z,
            piezo,
            timestamp);
    delay(50);
  }
  if (DEBUGMODE) {
    displayDataNormal(accelmag_event, gyro_event);
  }
}

//Creates and sends OSC packet
void sendData(double ax, 
              double ay, 
              double az, 
              double gx, 
              double gy, 
              double gz, 
              double piezo, 
              double timestamp) {
                
                msg.add( (float) ax);
                msg.add( (float) ay);
                msg.add( (float) az);
                msg.add( (float) gx);
                msg.add( (float) gy);
                msg.add( (float) gz);
                msg.add( (float) piezo);
                msg.add( (float) timestamp);
                
                udp.beginPacket(host, port);
                msg.send(udp);
                udp.endPacket();
                msg.empty();
}

void displayDataNormal(sensors_event_t accelmag_event, sensors_event_t gyro_event) {
  Serial.print(accelmag_event.acceleration.x);
  Serial.print(",");
  Serial.print(accelmag_event.acceleration.y);
  Serial.print(",");
  Serial.print(accelmag_event.acceleration.z);
  Serial.print(",");
  Serial.print(gyro_event.gyro.x);
  Serial.print(",");
  Serial.print(gyro_event.gyro.y);
  Serial.print(",");
  Serial.print(gyro_event.gyro.z);
  Serial.print(",");
  Serial.print(piezo);
  Serial.print(",");
  Serial.println(timestamp);
}
