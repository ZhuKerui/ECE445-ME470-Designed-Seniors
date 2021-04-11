#ifndef KEEBOT_SERIAL_SERVO_H
#define KEEBOT_SERIAL_SERVO_H

/**
 * Generate the command to control serial servos
 * @params: int len: length of the argument list, 3*num_servos
 * @params: ... servo instructions, e.g. index1, pwmv1, timev1, index2, pwmv2, timev2 ...
 */

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <common.h>
#include <keebot_led.h>
class Serial_Servo
{
private:
    SoftwareSerial servo_port;
    int ss_cmd_angle[NUM_SERVO_PER_LIMB];
    char cmd_return[200];
    int id_offset;
public:
    Serial_Servo(int rx_pin, int tx_pin, int id_offset = 0);
    void setup_baud(int32_t baud_rate);
    void init();
    void send_cmd(int len, ...);
    void send_cmd_in_range(int idx_low, int idx_high, int timev);
    void send_cmd_from_angle(int angle[NUM_SERVO_PER_LIMB]);
};

#endif
