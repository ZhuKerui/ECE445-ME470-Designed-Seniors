/******************************************************************************************************
 * 单片机：mega328p-au 外部晶振：16M 
********************************************************************************************/
#include <SoftwareSerial.h>    //包含软串口头文件，硬串口通信文件库系统自带                                                                                                                                                                                                                                                                                                                                                                                                                                                  String uart1_receive_buf = "";
/*******************************一些宏定义****************************************/
SoftwareSerial mySerial(A4,A5); //创建一个软串口的类，模拟引脚4,5分别代表 RX, TX引脚 AR多功能板

int myId, myPwm, myTime;
char cmd_return[100];//这里的cmd_return的字符长度要足够的大，根据舵机个数定，大小 = 15*个数+10
   
void setup() {
    Serial.begin(115200);           //硬件串口
    mySerial.begin(115200);         //设置软串口波特率
}
//这里我们实验软硬件串口 用户可根据实际情况定
void loop() {
        Serial.print("#000P0500T1000!");    //硬件串口 串口1 让0号舵机旋转到0500的位置 舵机的位置范围 500~2500
        Serial.print("#000P0500T1000");   //软串口 总线口 让0号舵机旋转到0500的位置 舵机的位置范围 500~2500
        delay(1000);                     //延时1秒  
        Serial.print("#000P2500T1000!");    //串口1 让0号舵机旋转到2500的位置 舵机的位置范围 500~2500
        Serial.print("#000P2500T1000!");  //总线口 让0号舵机旋转到2500的位置 舵机的位置范围 500~2500
        delay(1000);                     //延时1秒  
        
        //0号舵机用 变量控制 单个舵机控制
        myId = 0;
        myTime = 0;
        for(myPwm=500;myPwm<2500;myPwm++) {
            sprintf(cmd_return, "#%03dT%04dT%04d!", myId, myPwm, myTime);
            Serial.print(cmd_return);
            mySerial.print(cmd_return);
            delay(1);                        //延时1秒
        }
        
        //0号 1号 舵机用 变量控制 多个舵机控制 加{}
        myId = 0;
        myTime = 0;
        for(myPwm=500;myPwm<2500;myPwm++) {
            sprintf(cmd_return, "{#%03dT%04dT%04d!#%03dT%04dT%04d!}", myId, myPwm, myTime, myId+1, myPwm, myTime);
            delay(1);                        //延时1秒
            Serial.print(cmd_return);
            mySerial.print(cmd_return);
        }
    
}






