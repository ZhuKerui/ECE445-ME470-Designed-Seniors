#include <Arduino.h>
#include "keebot_uart.h"

void setup_serial_read() {
    uart_rcv_str.reserve(UART_RCV_STR_MAX_LEN);  // reserve 200 bytes for the incoming string
    uart_rcv_str = "";
    uart_rcv_begin = uart_rcv_complete = false;
    release_timetick = read_timetick = millis();
}

void serial_read(int index) {

    // release
    if(millis() - release_timetick > 3000) {
        release_timetick = millis();
        sprintf(cmd_return, "#%03dPULK!", index);
        Serial.println(cmd_return);
    }

    // read angle
    if(millis() - read_timetick > 1000) {
        read_timetick = millis();
        sprintf(cmd_return, "#%03dPRAD!", index);
        Serial.println(cmd_return);
    }
    
    // process returned string
    if (uart_rcv_complete) {
        int index, pwmv;
        if(uart_rcv_str[0] =='#' && uart_rcv_str[4] =='P' && uart_rcv_str[9] =='!') {
            index = (uart_rcv_str[1] - '0')*100 +  (uart_rcv_str[2] - '0')*10 +  (uart_rcv_str[3] - '0')*1;
            pwmv =  (uart_rcv_str[5] - '0')*1000 + (uart_rcv_str[6] - '0')*100 +  (uart_rcv_str[7] - '0')*10 +  (uart_rcv_str[8] - '0')*1;
            sprintf(cmd_return, "index = %03d  pwmv = %04d", index, pwmv);
            Serial.println(cmd_return);
        }
        
        uart_rcv_begin = false;
        uart_rcv_complete = false;
        uart_rcv_str = "";
    }
}

void serialEvent() {
    while (Serial.available()) {
        // Serial.print(1);
        char inChar = (char)Serial.read();  // get the new byte
        
        if (uart_rcv_complete) return;  // resume serial read after processing is done

        // a read begins
        if ( !uart_rcv_begin && inChar == '#' ) {
            uart_rcv_begin = true;
            uart_rcv_complete = false;
            uart_rcv_str = "";
        }
        
        // add it to the inputString:
        uart_rcv_str += inChar;

        // the current read completes
        if ( uart_rcv_begin && inChar == '!' ) {
            uart_rcv_complete = true;
        }

        // error occurs, str too long, then reset
        if (uart_rcv_str.length() > UART_RCV_STR_MAX_LEN) {
            uart_rcv_begin = false;
            uart_rcv_complete = false;
            uart_rcv_str = "";
        }
    }
}

void serial_servo_go(int len, ...) {
    va_list ap;
    va_start(ap,len);
    int index, pwmv, timev;
    
    strcpy(cmd_return, "{");
    for (int i=0; i<len/3; i++) {
        char cmd[15];
        index = va_arg(ap,int); pwmv = va_arg(ap,int); timev = va_arg(ap,int);
        sprintf(cmd, "#%03dP%04dT%04d!", index, pwmv, timev);
        strcat(cmd_return, cmd);
    }
    strcat(cmd_return, "}");

    Serial.println(cmd_return);
}