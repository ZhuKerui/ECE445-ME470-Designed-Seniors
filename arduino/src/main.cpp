#include <Arduino.h>
#include <SoftwareSerial.h>
#include <common.h>
#include <keebot_bluetooth.h>
#include <keebot_led.h>
#include <keebot_serial_servo.h>

Serial_Servo serial_servo_0(4, 5, ID_OFFSET_0); // RX,TX
Serial_Servo serial_servo_1(6, 7, ID_OFFSET_1); // RX,TX
Serial_Servo serial_servo_2(8, 9, ID_OFFSET_2); // RX,TX
Serial_Servo serial_servo_3(10, 11, ID_OFFSET_3); // RX,TX
Bluetooth bluetooth(2, 3); // RX,TX
int angle[NUM_SERVO];
int target_time;

float BT_SS_MAP_K[NUM_SERVO], BT_SS_MAP_B[NUM_SERVO];



// char output[100];

void setup() {
    Serial.begin(115200);
    serial_servo_0.setup_baud(SERVO_BAUD_RATE);
    serial_servo_1.setup_baud(SERVO_BAUD_RATE);
    serial_servo_2.setup_baud(SERVO_BAUD_RATE);
    serial_servo_3.setup_baud(SERVO_BAUD_RATE);
    // BLuetooth should be setup the last, because only the last setup software serial is listening.
    bluetooth.setup_baud(BLUETOOTH_BAUD_RATE);
    led_setup();

    // serial_servo_0.init();
    // serial_servo_1.init();
    // serial_servo_2.init();
    // serial_servo_3.init();
    
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

    for (int i = 0; i < NUM_SERVO; i++) {
        angle[i] = SERIAL_SERVO_LOW[i];
    }
    serial_servo_0.send_cmd_from_angle(angle, SERIAL_SERVO_DEFAULT_TIME);
    serial_servo_1.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*1), SERIAL_SERVO_DEFAULT_TIME);
    serial_servo_2.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*2), SERIAL_SERVO_DEFAULT_TIME);
    serial_servo_3.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*3), SERIAL_SERVO_DEFAULT_TIME);

    delay(3000);

    for (int i = 0; i < NUM_SERVO; i++) {
        angle[i] = SERIAL_SERVO_HIGH[i];
    }

    serial_servo_0.send_cmd_from_angle(angle, SERIAL_SERVO_DEFAULT_TIME);
    serial_servo_1.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*1), SERIAL_SERVO_DEFAULT_TIME);
    serial_servo_2.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*2), SERIAL_SERVO_DEFAULT_TIME);
    serial_servo_3.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*3), SERIAL_SERVO_DEFAULT_TIME);

    delay(3000);
// Loop Code
    // bluetooth.read_data();
    // if (bluetooth.data_available) {
    //     bluetooth.data_available = false;
    //     for (int i = 0; i < NUM_SERVO; i++) {
    //         angle[i] = (int)(BT_SS_MAP_K[i] * bluetooth.bt_msg[i] + BT_SS_MAP_B[i]);
    //     }
    //     target_time = ((int)bluetooth.bt_msg[BLE_MSG_LENGTH-1]) * 100;
    //     serial_servo_0.send_cmd_from_angle(angle, target_time);
    //     serial_servo_1.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*1), target_time);
    //     serial_servo_2.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*2), target_time);
    //     serial_servo_3.send_cmd_from_angle(angle+(NUM_SERVO_PER_LIMB*3), target_time);
    // }

    led_blink(3);
}
