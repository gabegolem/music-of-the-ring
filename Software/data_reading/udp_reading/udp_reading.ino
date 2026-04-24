#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <esp_now.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <SPI.h>
#include <OSCMessage.h>
#include <cppQueue.h>

#define OVERWRITE true

//Board/Pins
int piezo_pin = A2;


//Data
typedef struct __attribute__((packed)) struct_reading {
    double acceleration_x;
    double acceleration_y;
    double acceleration_z;
    double gyro_x;
    double gyro_y;
    double gyro_z;
    double piezo;
    double timestamp;
} struct_reading;

double timestamp;
double piezo;
struct_reading reading;


//Queue
cppQueue data_queue(sizeof(struct_reading), 20, FIFO, OVERWRITE);

//Network
WiFiUDP udp;
char *address = "/modeling";
OSCMessage msg(address);
//OSCMessage testmsg(address);

const char* ssid = "EAE";
//const char* ssid = "bucknell_iot";
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

  // Displays sensor details, indicating successful setup
  displaySensorDetails();
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

  
  if (piezo > 200) {
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
  
  displayDataNormal(accelmag_event, gyro_event);
}

/*                                         
void sendTest(float t) {
  
  testmsg.add(t);
  udp.beginPacket(host,port);
  testmsg.send(udp);
  udp.endPacket();
  testmsg.empty();
}
*/

struct_reading getReading(sensors_event_t accelmag_event, sensors_event_t gyro_event) {
  struct_reading new_reading;
  new_reading.acceleration_x = accelmag_event.acceleration.x;
  new_reading.acceleration_y = accelmag_event.acceleration.y;
  new_reading.acceleration_z = accelmag_event.acceleration.z;
  new_reading.gyro_x = gyro_event.gyro.x;
  new_reading.gyro_y = gyro_event.gyro.y;
  new_reading.gyro_z = gyro_event.gyro.z;
  new_reading.piezo = piezo;
  new_reading.timestamp = timestamp;
  return new_reading;
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
                
                Serial.println(udp.beginPacket(host, port));
                msg.send(udp);
                Serial.println(udp.endPacket());
                msg.empty();
}

// Displays data reading to serial for debugging purposes
void displayDataFancy(sensors_event_t accelmag_event, sensors_event_t gyro_event) {
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
  Serial.println("m/s^2");
  Serial.print("PIEZO: ");
  Serial.println(piezo);
  Serial.print("TIMESTAMP: ");
  Serial.println(timestamp);
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


// prints stats of sensor components
void displaySensorDetails(void) {

  sensor_t gyro_sensor;
  sensor_t accelmag_sensor;

  accelmag.getSensor(&accelmag_sensor);
  gyro.getSensor(&gyro_sensor);
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
  Serial.println("");
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
  delay(500);
}
