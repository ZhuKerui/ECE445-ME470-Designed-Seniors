#include <Arduino.h>

#define UART_RCV_STR_MAX_LEN    200

char cmd_return[101];           // TODO: may need to increase the length needed
unsigned long release_timetick, read_timetick;
String uart_rcv_str;            // A String to hold incoming data from uart
bool uart_rcv_begin, uart_rcv_complete;     // Whether read has begun/completed

void setup_serial_read();

void serial_read(int index);

/**
 * Generate the command to control serial servos
 * @params: int len: length of the argument list, 3*num_servos
 * @params: ... servo instructions, e.g. index1, pwmv1, timev1, index2, pwmv2, timev2 ...
 */
void serial_servo_go(int len, ...);