//#include <SoftwareSerial.h>    //包含软串口头文件，硬串口通信文件库系统自带                                                                                                                                                                                                                                                                                                                                                                                                                                                  String uart1_receive_buf = "";
//SoftwareSerial mySerial(10, 11); // 创建软串口 RX, TX

//#include "HD.h"
//#define comPin 4
//SoftwareSerialWithHalfDuplex HDport(comPin,comPin,false,false);

char cmd_return[101]; // TODO: may need to increase the length needed

void setup() {
  Serial.begin(115200);
//  HDport.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  led_blink(3);

  setup_serial_read();
}


void loop() {
//  Serial.println("#000PID111!"); // 将舵机ID000修改为ID111
//    led_on();
//    Serial.println(char(Serial.read()));

  serial_servo_go(6, 0,1200,500, 111,2000,500 );
  delay(2000);
  serial_servo_go(6, 0,1800,500, 111,1200,1000 );
  delay(2000);

//  serial_read(0);

}
