/*----------------------------------------------------------------------------
    关于设置类的都放在这个标签    
------------------------------------------------------------------------------*/
/*************************************************************
函数名：loop_nled()
功能介绍：LED灯闪烁，每秒闪烁一次
函数参数：无
返回值：  无
*************************************************************/
void loop_nled() {
    static u8 val = 0;
    static unsigned long systick_ms_bak = 0;
    if(millis() - systick_ms_bak > 500) {
      systick_ms_bak = millis();
      if(val) {
        nled_on();
      } else {
        nled_off();  
      }
      val = !val;
    }
}

void loop_read() {
   static long long systick_ms_bak = 0;
   static int index = 0, pwmv = 1500, timev = 0;
   static bool flag = false;

   //循环发送角度
   if(millis() - systick_ms_bak > 1000) {
      systick_ms_bak = millis();
      Serial.println("#000PRAD!");
   }
}



/*************************************************************
函数名：loop_uart()
功能介绍：解析串口接收到的字符串指令  
函数参数：无
返回值：  无
*************************************************************/
void loop_uart(){
     int index, pwmv;
    if(uart1_get_ok) {
        //打印字符串，测试的时候可以用
        Serial.print(uart_receive_str);
        //转换成字符串数组
        uart_receive_str.toCharArray(uart_receive_buf, uart_receive_str.length()+1);
        
        if(uart1_mode == 1) {
            //读取的角度格式是 #000P1500! 这种格式，所以我们只需对这种格式进行解析就可以了 满足这个格式就是正确的数据   
            if(uart_receive_buf[0] =='#' && uart_receive_buf[4] =='P' && uart_receive_buf[9] =='!') {
                index = (uart_receive_buf[1] - '0')*100 +  (uart_receive_buf[2] - '0')*10 +  (uart_receive_buf[3] - '0')*1;
                pwmv =  (uart_receive_buf[5] - '0')*1000 + (uart_receive_buf[6] - '0')*100 +  (uart_receive_buf[7] - '0')*10 +  (uart_receive_buf[8] - '0')*1;
                sprintf(cmd_return, "index = %03d  pwmv = %04d", index, pwmv);
                Serial.println(cmd_return);
            }
        }
        uart1_get_ok = 0;
        uart1_mode = 0;
        uart_receive_str = "";
    }
}  

/*************************************************************
函数名：serialEvent()
功能介绍：接收串口发来的字符串
函数参数：无
返回值：  无
*************************************************************/
void serialEvent() {
    static char sbuf_bak;
    while(Serial.available())  {      //
        sbuf_bak = char(Serial.read());      
        
        if(uart1_get_ok) return;
        if(uart1_mode == 0) {
          if(sbuf_bak == '#') {
            uart1_mode = 1;
          }  
          uart_receive_str = "";
        }
        
        uart_receive_str  += sbuf_bak;
        
        if((uart1_mode == 1) && (sbuf_bak == '!')){
          uart1_get_ok = 1;
        } 
        
        if(uart_receive_str.length() > 168) {
            uart_receive_str = "";
        }
    }
}
