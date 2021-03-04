/*----------------------------------------------------------------------------
    所有变量的定义   
------------------------------------------------------------------------------*/

#define  LED_PIN    13              //宏定义工作指示灯引脚
#define  BEEP_PIN   12

#define nled_on() {digitalWrite(LED_PIN, LOW);}
#define nled_off() {digitalWrite(LED_PIN, HIGH);}

#define beep_on() {digitalWrite(BEEP_PIN, LOW);}
#define beep_off() {digitalWrite(BEEP_PIN, HIGH);}


char buffer[168];                 // 定义一个数组用来存储每小组动作组
String uart_receive_str = "";    //声明一个字符串数组
char uart1_get_ok = 0, uart1_mode=0;
char cmd_return[64];
char uart_receive_buf[168];
void(* resetFunc) (void) = 0;


/*************************************************************
函数名称：abs_int(int t)
功能介绍：输入一个数值，返回一个数的绝对值
函数参数：t 要输入的数值  
返回值：  输入数的绝对值
*************************************************************/
int abs_int(int t) {
    if(t > 0)return t;
    return (-t);    
}

/*************************************************************
函数名称：selection_sort(int *a, int len)
功能介绍：对 a 数进行排序
函数参数：a 要排序是的数  
返回值：  len 输入数的个数
*************************************************************/
void selection_sort(int *a, int len) {
    int i,j,mi,t;
    for(i=0;i<len-1;i++) {
        mi = i;
        for(j=i+1;j<len;j++) {
            if(a[mi] > a[j]) {
                mi = j;    
            }    
        }    

        if(mi != i) {
            t = a[mi];
            a[mi] = a[i];
            a[i] = t;    
        }
    }
}

/*************************************************************
函数名称：str_contain_str(u8 *str, u8 *str2)
功能介绍：查询str是包含str2，并返回最后一个字符所在str的位置
函数参数：a 要排序是的数  
          len 输入数的个数
返回值： 返回最后一个字符所在str的位置 
*************************************************************/
u16 str_contain_str(u8 *str, u8 *str2) {
  u8 *str_temp, *str_temp2;
  str_temp = str;
  str_temp2 = str2;
  while(*str_temp) {
    if(*str_temp == *str_temp2) {
      while(*str_temp2) {
        if(*str_temp++ != *str_temp2++) {
          str_temp = str_temp - (str_temp2-str2) + 1;
          str_temp2 = str2;
          break;
        } 
      }
      if(!*str_temp2) {
        return (str_temp-str);
      }
    } else {
      str_temp++;
    }
  }
  return 0;
}
