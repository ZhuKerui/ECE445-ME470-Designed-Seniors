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
#define SET_ANGLE_COMMAND           "#%03dP%04dT%04d!"
#define BLUETOOTH_BAUD_RATE         9600
#define SERVO_BAUD_RATE             115200

const int BT_HIGH[BLE_MSG_LENGTH] = {180,  180,  180,  135,             // Right Arm
                                     180,  180,  180,  135,             // Right Leg
                                     180,  180,  180,  135,             // Left Arm
                                     180,  180,  180,  135,             // Left Leg
                                     50};                               // Interval

// const int SERIAL_SERVO_LOW[NUM_SERVO] = {2100, 2150, 2150, 825, 2100, 2150, 2150, 825, 2100, 2150, 2150, 825, 2100, 2150, 2150, 825};
// const int SERIAL_SERVO_HIGH[NUM_SERVO] = {850,  850,  850,  1800,  850,  850,  850,  1800,  850,  850,  850,  1800,  850,  850,  850,  1800};
const int SERIAL_SERVO_LOW[NUM_SERVO] = {2150,      2150,   2150,   825,    // Right Arm
                                         2150,      900,    850,    900,    // Right Leg
                                         2100,      2150,   2150,   825,    // Left Arm To Do
                                         2150,      800,    2150,   850};   // Left Leg

const int SERIAL_SERVO_HIGH[NUM_SERVO] = {850,      850,    850,    1800,     // Right Arm
                                          875,      2200,   2150,   1800,     // Right Leg
                                          850,      850,    850,    1800,     // Left Arm To Do
                                          900,      2100,   850,    1750};    // Left Leg

#endif
