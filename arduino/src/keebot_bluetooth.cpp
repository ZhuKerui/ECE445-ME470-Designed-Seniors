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
        delay(15);
        // Serial.println("fsfd");
        
        uint8_t angle = (uint8_t) bluetooth_port.read();
        if (angle == 0) {
            data_available = true;
            for (int i = 0; i < NUM_SERVO; i++) {
                angle = (uint8_t) bluetooth_port.read();
                if (angle >= BT_LOW && angle <= BT_HIGH[i]) {
                    bt_servo_angle[i] = angle;
                } else {
                    data_available = false;
                    // Serial.println("Fail");
                    break;
                }
            }
        }
    }
}
