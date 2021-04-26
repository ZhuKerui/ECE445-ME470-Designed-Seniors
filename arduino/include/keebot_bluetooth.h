#ifndef KEEBOT_BLUETOOTH_H
#define KEEBOT_BLUETOOTH_H

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <common.h>

class Bluetooth {
    public:
    Bluetooth(int rx_pin, int tx_pin);
    void setup_baud(int32_t baud_rate);
    bool data_available;
    uint8_t bt_msg[BLE_MSG_LENGTH];
    void read_data();

    private:
    SoftwareSerial bluetooth_port;
};

#endif
