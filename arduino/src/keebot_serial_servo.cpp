#include <keebot_serial_servo.h>

Serial_Servo::Serial_Servo(int rx_pin, int tx_pin, int id_offset) : servo_port(rx_pin, tx_pin), id_offset(id_offset) {}

void Serial_Servo::setup_baud(int32_t baud_rate) {
    servo_port.begin(baud_rate);
}

void Serial_Servo::send_cmd(int len, ...) {
    va_list ap;
    va_start(ap,len);
    int index, pwmv, timev;
    char cmd[30];

    strcpy(cmd_return, "{");
    for (int i = 0; i<len/3; i++) {
        index = va_arg(ap,int); pwmv = va_arg(ap,int); timev = va_arg(ap,int);
        sprintf(cmd, SET_ANGLE_COMMAND, index + id_offset, pwmv, timev);
        strcat(cmd_return, cmd);
    }
    strcat(cmd_return, "}");

    Serial.println(cmd_return);
    servo_port.println(cmd_return);
}

void Serial_Servo::send_cmd_in_range(int idx_low, int idx_high, int timev) {
    strcpy(cmd_return, "{");
    char cmd[30];

    for (int i = idx_low; i<idx_high; i++) {
        sprintf(cmd, SET_ANGLE_COMMAND, i + id_offset, ss_cmd_angle[i], timev);
        strcat(cmd_return, cmd);
    }
    strcat(cmd_return, "}");

    Serial.println(cmd_return);
    servo_port.println(cmd_return);
}

void Serial_Servo::init() {
    led_blink(2);
    for (int i = 0; i < NUM_SERVO_PER_PORT; i++){
        ss_cmd_angle[i] = SERIAL_SERVO_LOW[i];
    }
    delay(1000);
    send_cmd_in_range(0, NUM_SERVO_PER_PORT, SERIAL_SERVO_DEFAULT_TIME);
}

void Serial_Servo::send_cmd_from_angle(int angle[NUM_SERVO_PER_PORT], int target_time) {
    for (int i = 0; i < NUM_SERVO_PER_PORT; i++) {
        if ((angle[i] >= SERIAL_SERVO_LOW[i+id_offset-1] && angle[i] <= SERIAL_SERVO_HIGH[i+id_offset-1]) 
         || (angle[i] <= SERIAL_SERVO_LOW[i+id_offset-1] && angle[i] >= SERIAL_SERVO_HIGH[i+id_offset-1])){
            ss_cmd_angle[i] = angle[i];
        }
    }
    send_cmd_in_range(0, NUM_SERVO_PER_PORT, target_time);
}
