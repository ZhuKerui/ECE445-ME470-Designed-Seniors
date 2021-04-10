#include <keebot_led.h>

void led_setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    led_blink(2);
}

void led_on() {digitalWrite(LED_BUILTIN, HIGH);}

void led_off() {digitalWrite(LED_BUILTIN, LOW);}

void led_blink(int t) {
    delay(1000);
    for (int i=0; i<t; i++) {
      led_on();delay(300);led_off();delay(300);
    }
}
