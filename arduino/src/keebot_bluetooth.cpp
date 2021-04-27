#include <keebot_bluetooth.h>
#include <keebot_led.h>

Bluetooth::Bluetooth(int rx_pin, int tx_pin) : bluetooth_port(rx_pin, tx_pin) {
    data_available = false;
}

void Bluetooth::setup_baud(int32_t baud_rate) {
    bluetooth_port.begin(baud_rate);
}

void Bluetooth::read_data() {

    if(bluetooth_port.available() > 0) {
        delay(20);
        uint8_t data = (uint8_t) bluetooth_port.read();
        if (data == 0) {
            data_available = true;
            for (int i = 0; i < BLE_MSG_LENGTH; i++) {
                data = (uint8_t) bluetooth_port.read();
                if (data >= BT_LOW && data <= BT_HIGH[i]) {
                    bt_msg[i] = data;
                } else {
                    data_available = false;
                    break;
                }
            }
        }
    }
}
