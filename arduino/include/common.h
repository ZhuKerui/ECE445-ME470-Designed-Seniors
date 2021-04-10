#ifndef COMMON_H
#define COMMON_H

#define NUM_SERVO   4
#define ID_OFFSET   1
#define BT_LOW      1
#define SERIAL_SERVO_TIME 1000
#define SET_ANGLE_COMMAND   "#%03dP%04dT%04d!"
#define BLUETOOTH_BAUD_RATE     9600
#define SERVO_BAUD_RATE         115200

const int BT_HIGH[NUM_SERVO] = {180,  180,  180,  135};
const int SERIAL_SERVO_LOW[NUM_SERVO] = {2100, 2150, 2150, 825};
const int SERIAL_SERVO_HIGH[NUM_SERVO] = {850,  850,  850,  1800};

#endif