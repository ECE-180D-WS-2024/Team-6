#include <WiFi.h>
#include <PubSubClient.h>
#include "arduino_secrets.h"
#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU

//#define USE_SPI // Uncomment this to use SPI

#define SERIAL_PORT Serial

#define SPI_PORT SPI // Your desired SPI port. Used only when "USE_SPI" is defined
#define CS_PIN 2 // Which pin you connect CS to. Used only when "USE_SPI" is defined

#define WIRE_PORT Wire // Your desired Wire port. Used when "USE_SPI" is not defined
// The value of the last bit of the I2C address.
// On the SparkFun 9DoF IMU breakout, the default is 1, and when the ADR jumper is closed, the value becomes 0
#define AD0_VAL 1

#ifdef USE_SPI
ICM_20948_SPI myICM; // If using SPI, create an ICM_20948_SPI object
#else
ICM_20948_I2C myICM; // Otherwise, create an ICM_20948_I2C object
#endif

// WiFi
const char *ssid = SECRET_SSID; // Enter your WiFi name
const char *password = SECRET_PASS; // Enter WiFi password

// MQTT Broker
// const char *mqtt_broker = "broker.emqx.io";
// const char *topic = "ece180d/test";
// const char *mqtt_username = "emqx";
// const char *mqtt_password = "public";
// const int mqtt_port = 1883;

// MQTT Broker
const char *mqtt_broker = "mqtt.eclipseprojects.io";
const char *topic1 = "ece180d/team6/johanna";
const char *topic2 = "ece180d/test/team6";
// const char *mqtt_username = "emqx";
// const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  // Set software serial baud to 115200;
  Serial.begin(115200);
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  // connecting to an MQTT broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
    String client_id = "esp32-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
    if (client.connect(client_id.c_str())) { //, mqtt_username, mqtt_password)) {
      Serial.println("mqtt broker connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  // publish and subscribe
  client.publish(topic1, "Hi, I’m ESP32 ^^");
  client.subscribe(topic2);

#ifdef USE_SPI
  SPI_PORT.begin();
#else
  WIRE_PORT.begin();
  WIRE_PORT.setClock(400000);
#endif

  bool initialized = false;
  while (!initialized) {
#ifdef USE_SPI
    myICM.begin(CS_PIN, SPI_PORT);
#else
    myICM.begin(WIRE_PORT, AD0_VAL);
#endif

    SERIAL_PORT.print(F("Initialization of the sensor returned: "));
    SERIAL_PORT.println(myICM.statusString());
    if (myICM.status != ICM_20948_Stat_Ok) {
      SERIAL_PORT.println("Trying again...");
      delay(500);
    } else {
      initialized = true;
    }
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

void loop() {
  if (myICM.dataReady()) {
    myICM.getAGMT(); // The values are only updated when you call ’getAGMT’
    // printRawAGMT( myICM.agmt ); // Uncomment this to see the raw values, taken directly from the agmt structure
    printScaledAGMT(&myICM); // This function takes into account the scale settings from when
                             // the measurement was made to calculate the values with units
     //client.publish(topic, myICM->acc.axes.x);
     client.loop();
     delay(100);

//    int16_t ax = myICM.accX();
//    int16_t ay = myICM.accY();
//    int16_t az = myICM.accZ();
//    int16_t gx = myICM.gyrX();
//    int16_t gy = myICM.gyrY();
//    int16_t gz = myICM.gyrZ();
//
//    // Create JSON payload
//    String payload = "{\"acceleration\":{\"x\":" + String(ax) + ",\"y\":" + String(ay) + ",\"z\":" + String(az) +
//                    "},\"gyroscope\":{\"x\":" + String(gx) + ",\"y\":" + String(gy) + ",\"z\":" + String(gz) + "}}";
//
//    // Publish data to MQTT topic
//    client.publish(topic1, payload.c_str());
//    client.loop();
//    delay(30);


  } else {
    SERIAL_PORT.println("Waiting for data");
    client.loop();
    delay(500);
  }
}

// Below here are some helper functions to print the data nicely!

void printPaddedInt16b(int16_t val) {
  if (val > 0) {
    SERIAL_PORT.print(" ");
    if (val < 10000) {
      SERIAL_PORT.print("0");
    }
    if (val < 1000) {
      SERIAL_PORT.print("0");
    }
    if (val < 100) {
      SERIAL_PORT.print("0");
    }
    if (val < 10) {
      SERIAL_PORT.print("0");
    }
  } else {
    SERIAL_PORT.print("-");
    if (abs(val) < 10000) {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 1000) {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 100) {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 10) {
      SERIAL_PORT.print("0");
    }
  }
  SERIAL_PORT.print(abs(val));
}

void printRawAGMT(ICM_20948_AGMT_t agmt) {
  SERIAL_PORT.print("RAW. Acc [ ");
  printPaddedInt16b(agmt.acc.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.acc.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.acc.axes.z);
  SERIAL_PORT.print(" ], Gyr [ ");
  printPaddedInt16b(agmt.gyr.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.gyr.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.gyr.axes.z);
  SERIAL_PORT.print(" ], Mag [ ");
  printPaddedInt16b(agmt.mag.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.mag.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.mag.axes.z);
  SERIAL_PORT.print(" ], Tmp [ ");
  printPaddedInt16b(agmt.tmp.val);
  SERIAL_PORT.print(" ]");
  SERIAL_PORT.println();
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals) {
  float aval = abs(val);
  if (val < 0) {
    SERIAL_PORT.print("-");
  } else {
    SERIAL_PORT.print(" ");
  }
 

 for (uint8_t indi = 0; indi < leading; indi++) {
    uint32_t tenpow = 0;
    if (indi < (leading - 1)) {
      tenpow = 1;
    }
    for (uint8_t c = 0; c < (leading - 1 - indi); c++) {
      tenpow *= 10;
    }
    if (aval < tenpow) {
      SERIAL_PORT.print("0");
    } else {
      break;
    }
  }
  if (val < 0) {
    SERIAL_PORT.print(-val, decimals);
  } else {
    SERIAL_PORT.print(val, decimals);
  }
}

#ifdef USE_SPI
void printScaledAGMT(ICM_20948_SPI *sensor) {
#else
void printScaledAGMT(ICM_20948_I2C *sensor) {
#endif

  float ax = myICM.accX();
  float ay = myICM.accY();
  float az = myICM.accZ();
  float gx = myICM.gyrX();
  float gy = myICM.gyrY();
  float gz = myICM.gyrZ();

  SERIAL_PORT.print("Scaled. Acc (mg) [ ");
  printFormattedFloat(ax, 5, 2);
  char buf1[10];
  snprintf(buf1, 10, "%f", ax);
//  client.publish(topic1, buf);
  SERIAL_PORT.print(", ");
  printFormattedFloat(ay, 5, 2);
  char buf2[10];
  snprintf(buf2, 10, "%f", ay);
  SERIAL_PORT.print(", ");
  printFormattedFloat(az, 5, 2);
  char buf3[10];
  snprintf(buf3, 10, "%f", az);
  
  SERIAL_PORT.print(" ], Gyr (DPS) [ ");
  printFormattedFloat(gx, 5, 2);
  char buf4[10];
  snprintf(buf4, 10, "%f", gx);
  SERIAL_PORT.print(", ");
  printFormattedFloat(gy, 5, 2);
  char buf5[10];
  snprintf(buf5, 10, "%f", gy);
  SERIAL_PORT.print(", ");
  printFormattedFloat(gz, 5, 2);
  char buf6[10];
  snprintf(buf6, 10, "%f", gz);
  
  SERIAL_PORT.print(" ], Mag (uT) [ ");
  printFormattedFloat(sensor->magX(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->magY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->magZ(), 5, 2);
  SERIAL_PORT.print(" ], Tmp (C) [ ");
  printFormattedFloat(sensor->temp(), 5, 2);
  SERIAL_PORT.print(" ]");
  SERIAL_PORT.println();


    // Create JSON payload
    String payload = "{\"acceleration\":{\"x\":" + String(buf1) + ", \"y\":" + String(buf2) + ", \"z\":" + String(buf3) +
                    "},\"gyroscope\":{\"x\":" + String(buf4) + ",\"y\":" + String(buf5) + ",\"z\":" + String(buf6) + "}}";


    // Publish data to MQTT topic
    client.publish(topic1, payload.c_str());
    client.loop();
    delay(30);

  
}
