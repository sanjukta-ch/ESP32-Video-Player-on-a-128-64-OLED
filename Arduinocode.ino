#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "final1frames.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    OLED_RESET
);

void setup()
{
    Wire.begin();

    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

    display.clearDisplay();
    display.display();
}

void loop()
{
    for (int frame = 0; frame < FRAME_COUNT; frame++)
    {
        display.clearDisplay();

        display.drawBitmap(
            0,
            0,
            videoFrames + frame * FRAME_SIZE,
            FRAME_WIDTH,
            FRAME_HEIGHT,
            SSD1306_WHITE
        );

        display.display();

        delay(33);   // ~30 FPS
    }
}
