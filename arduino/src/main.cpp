#include <Arduino.h>
#include <keebot_bluetooth.h>
#include <keebot_led.h>
#include <keebot_serial_servo.h>

Serial_Servo serial_servo(5, 6); // RX,TX
Bluetooth bluetooth(2, 3); // RX,TX
int angle[NUM_SERVO];

float BT_SS_MAP_K[NUM_SERVO], BT_SS_MAP_B[NUM_SERVO];



// char output[100];

void setup() {
    Serial.begin(115200);
    serial_servo.setup_baud(SERVO_BAUD_RATE);
    bluetooth.setup_baud(BLUETOOTH_BAUD_RATE);
    led_setup();

    serial_servo.init();
    
    for (int i = 0; i < NUM_SERVO; i++) {
        BT_SS_MAP_K[i] = (SERIAL_SERVO_HIGH[i] - SERIAL_SERVO_LOW[i]) / (BT_HIGH[i] - BT_LOW);
        BT_SS_MAP_B[i] = SERIAL_SERVO_LOW[i] - BT_SS_MAP_K[i] * BT_LOW;
    }
}

void loop() {
    // put your main code here, to run repeatedly:
// Test3: Four Servos Test
//    serial_servo_go(12, 1, SERIAL_SERVO_HIGH[1] ,SERIAL_SERVO_TIME,
//                        2, SERIAL_SERVO_HIGH[2] ,SERIAL_SERVO_TIME,
//                        3, SERIAL_SERVO_HIGH[3] ,SERIAL_SERVO_TIME,
//                        4, SERIAL_SERVO_HIGH[4] ,SERIAL_SERVO_TIME);
//    delay(2000);

// Test2: Bluetooth Connection Test
//    if (btTest.available() > 0) {
//        uint8_t read_byte = (uint8_t) btTest.read();
//        sprintf(output, "%u, ", read_byte);
//        Serial.print(output);
//    }

// Test1: Periodic Test of One Servo
//      serial_servo_go(3, 2, SERIAL_SERVO_LOW[2], SERIAL_SERVO_TIME);
//      delay(2000);
//      serial_servo_go(3, 2, SERIAL_SERVO_HIGH[2], SERIAL_SERVO_TIME);
//      delay(2000);

// Loop Code
    bluetooth.read_data();
    if (bluetooth.data_available) {
        bluetooth.data_available = false;
        for (int i = 0; i < NUM_SERVO; i++) {
            angle[i] = (int)(BT_SS_MAP_K[i] * bluetooth.bt_servo_angle[i] + BT_SS_MAP_B[i]);
        }
        serial_servo.send_cmd_from_angle(angle);
    }
}
