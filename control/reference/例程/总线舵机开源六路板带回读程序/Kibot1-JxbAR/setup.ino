/*----------------------------------------------------------------------------
    关于设置类的都放在这个标签    
------------------------------------------------------------------------------*/

void setup_nled() {
    pinMode(LED_PIN,OUTPUT);               //设置引脚为输出模式
    digitalWrite(LED_PIN, HIGH );
}

void setup_beep() {
    pinMode(BEEP_PIN,OUTPUT); 
    digitalWrite(BEEP_PIN, HIGH );
}

void setup_uart() {
    Serial.begin(115200);                 //初始化波特率为115200
}

void setup_start() {
  beep_on();delay(100);beep_off();delay(100);
  beep_on();delay(100);beep_off();delay(100);
  beep_on();delay(100);beep_off();delay(100);
}

void setup_zx_servo() {//开机动作测试舵机
    static int index = 0, pwmv = 1500, timev = 0;
    index = 0; pwmv = 1700;timev = 200;
    sprintf(cmd_return, ">>>#%03dP%04dT%04d!", index, pwmv, timev);
    Serial.println(cmd_return);
    delay(1000);

    index = 0; pwmv = 1300;timev = 200;
    sprintf(cmd_return, ">>>#%03dP%04dT%04d!", index, pwmv, timev);
    Serial.println(cmd_return);
    delay(1000);

    index = 0; pwmv = 1500;timev = 200;
    sprintf(cmd_return, ">>>#%03dP%04dT%04d!", index, pwmv, timev);
    Serial.println(cmd_return);
    delay(1000);

    Serial.println("#000PULK!");delay(10);
    Serial.println("#000PULM!");
}
