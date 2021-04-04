#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Arduino.h>

#include <keebot_ble.h>
#include "keebot_uart.h"

uint8_t txValue = 0;

void setup() {
    Serial.begin(115200);
    Keebot_BLE::start("Keebot");
    Keebot_BLE::start_broadcasting();

    // setup_serial_read();
}

void loop() {

    if (Keebot_BLE::deviceConnected) {
        Keebot_BLE::send_data(&txValue, 1);
        txValue++;                                          // Increase the message value by one
        delay(1000);                                        // bluetooth stack will go into congestion, if too many packets are sent
    }

    // If disconnection happens
    if (!Keebot_BLE::deviceConnected && Keebot_BLE::oldDeviceConnected) {
        delay(500);                                         // Give some time for handling the disconnection
        Keebot_BLE::start_broadcasting();                        // Restart the boardcasting
    }
    
    // If connection happens
    if (Keebot_BLE::deviceConnected && !Keebot_BLE::oldDeviceConnected) {
        // do stuff here on connecting
    }

    // serial_servo_go(6, 0,1200,500, 111,2000,500 );
    // delay(2000);
    // serial_servo_go(6, 0,1800,500, 111,1200,1000 );
    // delay(2000);
    // serial_read(0);
}