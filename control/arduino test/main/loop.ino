
void led_on() {digitalWrite(LED_BUILTIN, HIGH);}
void led_off() {digitalWrite(LED_BUILTIN, LOW);}

void led_blink(int t) {
  for (int i=0; i<t; i++) {
    led_on();delay(300);led_off();delay(300);
  }
}


/**
 * Generate the command to control serial servos
 * @params: int len: length of the argument list, 3*num_servos
 * @params: ... servo instructions, e.g. index1, pwmv1, timev1, index2, pwmv2, timev2 ...
 */
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
  
//  if (HDport.available()) {
//    HDport.write("#000P1500T1000!");
//  }
//
//  delay(1500);
//  if (HDport.available()) {
//    HDport.write("#000P1200T1000!");
//  }
  
  
}
