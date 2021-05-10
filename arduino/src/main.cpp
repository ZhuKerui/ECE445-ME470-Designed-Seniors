#include <Arduino.h>
#include <SoftwareSerial.h>
#include <common.h>
#include <keebot_bluetooth.h>
#include <keebot_led.h>
#include <keebot_serial_servo.h>

Serial_Servo serial_up(4, 5, ID_OFFSET_0); // RX,TX
Serial_Servo serial_down(6, 7, ID_OFFSET_1); // RX,TX
Bluetooth bluetooth(2, 3); // RX,TX
int angle[NUM_SERVO];
int target_time;

float BT_SS_MAP_K[NUM_SERVO], BT_SS_MAP_B[NUM_SERVO];


// char output[100];

void setup() {
    Serial.begin(115200);
    serial_up.setup_baud(SERVO_BAUD_RATE);
    serial_down.setup_baud(SERVO_BAUD_RATE);
    // BLuetooth should be setup the last, because only the last setup software serial is listening.
    bluetooth.setup_baud(BLUETOOTH_BAUD_RATE);
    led_setup();

    // serial_up.init();
    // serial_down.init();

    
    for (int i = 0; i < NUM_SERVO; i++) {
        BT_SS_MAP_K[i] = (SERIAL_SERVO_HIGH[i] - SERIAL_SERVO_LOW[i]) / (BT_HIGH[i] - BT_LOW);
        BT_SS_MAP_B[i] = SERIAL_SERVO_LOW[i] - BT_SS_MAP_K[i] * BT_LOW;
    }
}

void loop() {
    // put your main code here, to run repeatedly:

// Test: calibration and initilization
    for (int i = 0; i < NUM_SERVO; i++) {
        angle[i] = SERIAL_SERVO_LOW[i];
    }
    serial_up.send_cmd_from_angle(angle, SERIAL_SERVO_DEFAULT_TIME);
    serial_down.send_cmd_from_angle(angle+(NUM_SERVO_PER_PORT*1), SERIAL_SERVO_DEFAULT_TIME);

    delay(3000);

    for (int i = 0; i < NUM_SERVO; i++) {
        angle[i] = SERIAL_SERVO_HIGH[i];
    }
    serial_up.send_cmd_from_angle(angle, SERIAL_SERVO_DEFAULT_TIME);
    serial_down.send_cmd_from_angle(angle+(NUM_SERVO_PER_PORT*1), SERIAL_SERVO_DEFAULT_TIME);

    delay(3000);


// Loop Code
    // bluetooth.read_data();
    // if (bluetooth.data_available) {
    //     bluetooth.data_available = false;
    //     for (int i = 0; i < NUM_SERVO; i++) {
    //         angle[i] = (int)(BT_SS_MAP_K[i] * bluetooth.bt_msg[i] + BT_SS_MAP_B[i]);
    //     }
    //     target_time = ((int)bluetooth.bt_msg[BLE_MSG_LENGTH-1]) * 100;
    //     Serial.println(target_time);
    //     serial_up.send_cmd_from_angle(angle, target_time);
    //     serial_down.send_cmd_from_angle(angle+(NUM_SERVO_PER_PORT*1), target_time);
    // }
}
