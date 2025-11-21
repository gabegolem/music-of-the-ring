#include <Adafruit_FXAS21002C.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <esp_now.h>
#include <WiFi.h>

int piezo_pin = A0;

typedef struct __attribute__((packed)) struct_readings {
    double acceleration_x;
    double acceleration_y;
    double acceleration_z;
    double gyro_x;
    double gyro_y;
    double gyro_z;
    double piezo;
} struct_readings;

// Create a variable of this type to store the data
struct_readings readings;
char * readings_bytes;
char * gyro_x_bytes;
char * gyro_y_bytes;

// Laptop's MAC Address (replace with the actual MAC address)
const char* ssid = "bucknell_iot";
uint8_t broadcastAddress[] = {0xdc, 0x21, 0x48, 0x82, 0x96, 0x82}; //mac address
const char* host = "10.98.148.138";//implement automatic grabbing of laptop ip
const uint16_t port = 8000;
bool itison = false;

/* Assign a unique ID to this sensor at the same time */
Adafruit_FXAS21002C imu = Adafruit_FXAS21002C(0x0021002C);

void displaySensorDetails(void) {

  sensor_t sensor;
  imu.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print("Sensor:       ");
  Serial.println(sensor.name);
  Serial.print("Driver Ver:   ");
  Serial.println(sensor.version);
  Serial.print("Unique ID:    0x");
  Serial.println(sensor.sensor_id, HEX);
  Serial.print("Max Value:    ");
  Serial.print(sensor.max_value);
  Serial.println(" rad/s");
  Serial.print("Min Value:    ");
  Serial.print(sensor.min_value);
  Serial.println(" rad/s");
  Serial.print("Resolution:   ");
  Serial.print(sensor.resolution);
  Serial.println(" rad/s");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

void setup(void) {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid);

  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("_");
  }
  Serial.println("");
  Serial.println(WiFi.SSID());

  /* Wait for the Serial Monitor */
  while (!Serial) {
    delay(1);
  }

  Serial.println("Gyroscope Test");
  Serial.println("");

  /* Initialise the sensor */
  if (!imu.begin()) {
    /* There was a problem detecting the FXAS21002C ... check your connections
     */
    Serial.println("Ooops, no FXAS21002C detected ... Check your wiring!");
    while (1)
      ;
  }

  /* Set gyro range. (optional, default is 250 dps) */
  // gyro.setRange(GYRO_RANGE_2000DPS);

  /* Display some basic information on this sensor */
  displaySensorDetails();
}

void loop(void) {

  if(itison) {
    delay(2000);
    return;
  }

  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("Connection Failed");
    delay(1000);
    return;
  }

  sensors_event_t event;
  imu.getEvent(&event);

  /* Display the results (speed is measured in rad/s) */

  readings.gyro_x = event.gyro.x;
  readings.gyro_y = event.gyro.y;
  readings.gyro_z = event.gyro.z;
  readings.acceleration_x = event.acceleration.x;
  readings.acceleration_y = event.acceleration.y;
  readings.acceleration_z = event.acceleration.z;
  readings.piezo = analogRead(piezo_pin);
  Serial.print("O");
  Serial.println(readings.piezo);
  readings_bytes = reinterpret_cast<char*>(&readings);
  
  while(client.available() > 0 || client.connected()>0) {
    //client.write(readings_bytes, sizeof(double) * 7);
    client.write(readings_bytes, 56);
  }
  delay(50);
  /* Get a new sensor event */
}

void displayIMUData(sensors_event_t event) {
  Serial.print("GYRO  ");
  Serial.print("X: ");
  Serial.print(event.gyro.x);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(event.gyro.y);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(event.gyro.z);
  Serial.print("  ");
  Serial.println("rad/s ");
  Serial.print("ACCELERATION  ");
  Serial.print("X: ");
  Serial.print(event.acceleration.x);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(event.acceleration.y);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(event.acceleration.z);
  Serial.print("  ");
  Serial.println("m/s^2");
}
