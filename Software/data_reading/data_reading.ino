#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
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
const char* ssid = "Home524";
const char* pword = "Home7777";
uint8_t broadcastAddress[] = {0xdc, 0x21, 0x48, 0x82, 0x96, 0x82}; //mac address
const char* host = "10.0.0.210";//implement automatic grabbing of laptop ip
const uint16_t port = 8000;
bool itison = false;

/* Assign a unique ID to this sensor at the same time */
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);

void displaySensorDetails(void) {

  sensor_t gyro_sensor;
  sensor_t accelmag_sensor;

  gyro.getSensor(&gyro_sensor);
  accelmag.getSensor(&accelmag_sensor);
  Serial.println("------------------------------------");
  Serial.print("Gyro-Sensor:       ");
  Serial.println(gyro_sensor.name);
  Serial.print("Driver Ver:   ");
  Serial.println(gyro_sensor.version);
  Serial.print("Unique ID:    0x");
  Serial.println(gyro_sensor.sensor_id, HEX);
  Serial.print("Max Value:    ");
  Serial.print(gyro_sensor.max_value);
  Serial.println(" rad/s");
  Serial.print("Min Value:    ");
  Serial.print(gyro_sensor.min_value);
  Serial.println(" rad/s");
  Serial.print("Resolution:   ");
  Serial.print(gyro_sensor.resolution);
  Serial.println(" rad/s");
  Serial.println("------------------------------------");
  Serial.println("");
  Serial.println("------------------------------------");
  Serial.print("Accelmag-Sensor:       ");
  Serial.println(accelmag_sensor.name);
  Serial.print("Driver Ver:   ");
  Serial.println(accelmag_sensor.version);
  Serial.print("Unique ID:    0x");
  Serial.println(accelmag_sensor.sensor_id, HEX);
  Serial.print("Max Value:    ");
  Serial.print(accelmag_sensor.max_value);
  Serial.println(" m/s^2");
  Serial.print("Min Value:    ");
  Serial.print(accelmag_sensor.min_value);
  Serial.println(" m/s^2");
  Serial.print("Resolution:   ");
  Serial.print(accelmag_sensor.resolution);
  Serial.println(" m/s^2");
  Serial.println("------------------------------------");
  delay(500);
}

void setup(void) {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pword);

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
  if (!gyro.begin()) {
    /* There was a problem detecting the FXAS21002C ... check your connections
     */
    Serial.println("Ooops, no FXAS21002C detected ... Check your wiring!");
    while (1)
      ;
  }

  gyro.setRange(GYRO_RANGE_2000DPS);

  Serial.println("Accelerometer Test");
  Serial.println("");

  /* Initialise the sensor */
  if (!accelmag.begin()) {
    /* There was a problem detecting the FXAS21002C ... check your connections
     */
    Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
    while (1)
      ;
  }

  accelmag.setAccelRange(ACCEL_RANGE_8G);
  accelmag.setSensorMode(ACCEL_ONLY_MODE);

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

  sensors_event_t accelmag_event;
  accelmag.getEvent(&accelmag_event);
  sensors_event_t gyro_event;
  gyro.getEvent(&gyro_event);

  /* Display the results (speed is measured in rad/s) */

  readings.gyro_x = gyro_event.gyro.x;
  readings.gyro_y = gyro_event.gyro.y;
  readings.gyro_z = gyro_event.gyro.z;
  readings.acceleration_x = accelmag_event.acceleration.x;
  readings.acceleration_y = accelmag_event.acceleration.y;
  readings.acceleration_z = accelmag_event.acceleration.z;
  readings.piezo = analogRead(piezo_pin);
  readings_bytes = reinterpret_cast<char*>(&readings);

  while(client.available() > 0 || client.connected()>0) {
    //client.write(readings_bytes, sizeof(double) * 7);
    client.write(readings_bytes, 56);
  }
  delay(2.5);

  displayData(gyro_event, accelmag_event);
  /* Get a new sensor event */
}

void displayData(sensors_event_t gyro_event, sensors_event_t accelmag_event) {
  Serial.print("GYRO  ");
  Serial.print("X: ");
  Serial.print(gyro_event.gyro.x);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(gyro_event.gyro.y);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(gyro_event.gyro.z);
  Serial.print("  ");
  Serial.println("rad/s ");
  Serial.print("ACCELERATION  ");
  Serial.print("X: ");
  Serial.print(accelmag_event.acceleration.x);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(accelmag_event.acceleration.y);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(accelmag_event.acceleration.z);
  Serial.print("  ");
  Serial.println("m/s^2");
}
