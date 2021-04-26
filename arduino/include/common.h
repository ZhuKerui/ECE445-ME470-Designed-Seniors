#ifndef COMMON_H
#define COMMON_H

#define NUM_SERVO           16
#define BLE_MSG_LENGTH      (NUM_SERVO+1)
#define NUM_SERVO_PER_LIMB  4
#define ID_OFFSET_0         1
#define ID_OFFSET_1         5
#define ID_OFFSET_2         9
#define ID_OFFSET_3         13

#define BT_LOW              1
#define SERIAL_SERVO_DEFAULT_TIME   1000
#define SET_ANGLE_COMMAND   "#%03dP%04dT%04d!"
#define BLUETOOTH_BAUD_RATE     9600
#define SERVO_BAUD_RATE         115200

const int BT_HIGH[BLE_MSG_LENGTH] = {180,  180,  180,  135,  180,  180,  180,  135,  180,  180,  180,  135,  180,  180,  180,  135,  50};
const int SERIAL_SERVO_LOW[NUM_SERVO] = {2100, 2150, 2150, 825, 2100, 2150, 2150, 825, 2100, 2150, 2150, 825, 2100, 2150, 2150, 825};
const int SERIAL_SERVO_HIGH[NUM_SERVO] = {850,  850,  850,  1800,  850,  850,  850,  1800,  850,  850,  850,  1800,  850,  850,  850,  1800};

#endif
