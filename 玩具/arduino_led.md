# Arduino LED

## 原件

硬件：

* Arduino UNO
* WS2812B

开源库：

* [FastLED](https://github.com/FastLED/FastLED)

## 原理

点亮一颗 LED：

```c
#include <FastLED.h>

#define NUM_LEDS 1

// 数据引脚
#define LED_PIN  7

CRGB leds[NUM_LEDS];

void setup()
{
  FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, NUM_LEDS);
}

void loop()
{
  int r = 255;
  int g = 255;
  int b = 0;
  // 设置颜色
  leds[0] = CRGB(r, g, b);
  // 设置亮度
  FastLED.setBrightness(br);
  FastLED.show();
}
```

串口通信：

```c

void setup() {
    // 设置波特率
    Serial.begin(9600);
}

// 串口事件监听
void serialEvent() {
    if (Serial.available() > 0) {
        char get = Serial.read();
        Serial.println(get, 8);
    }
}

void loop() {
}
```