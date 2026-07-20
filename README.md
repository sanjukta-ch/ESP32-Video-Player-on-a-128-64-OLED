# ESP32-Video-Player-on-a-128-64-OLED
Converts any MP4 video into a sequence of monochrome bitmap frames and plays it on an SSD1306 OLED using an ESP32.


## Project Overview

This project demonstrates how an ESP32 can be used to display a video on a tiny 128×64 monochrome OLED screen.

Since the SSD1306 display cannot decode compressed video formats such as MP4, AVI, or GIF, the video must first be converted into a sequence of bitmap frames. A Python script performs this conversion and generates an Arduino-compatible header file (`finalframes.h`) containing every frame packed into flash memory.

The ESP32 then reads each frame directly from flash using the `PROGMEM` attribute and displays them sequentially, creating the illusion of video playback.

---

## Demo



---

# Hardware

- ESP32 DevKit V1
- SSD1306 128×64 I²C OLED Display
- Breadboard
- Jumper wires
- USB cable

---

# Wiring

| OLED | ESP32 |
|------|-------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

---

# Software Requirements

## Python

Python 3.10+

Install dependencies:

```bash
pip install opencv-python numpy
```

Libraries used:

- OpenCV
- NumPy
- pathlib

---

## Arduino

Libraries required:

- Adafruit SSD1306
- Adafruit GFX Library
- Adafruit BusIO

These can be installed through the Arduino Library Manager or PlatformIO.

---

# Repository Structure

```
ESP32-OLED-Video/
│
├── Arduino/
│   ├── VideoPlayer.ino
│   ├── finalframes.h
│   └── platformio.ini
│
├── Python/
│   └── video_converter.py
│
├── media/
│   ├── original_video.mp4
│   ├── demo.gif
│   └── wiring.jpg
│
└── README.md
```

---

# How It Works

The project is split into two stages.

## Stage 1 — Video Conversion

The Python script

- Reads every frame of the source MP4.
- Converts each frame to grayscale.
- Resizes it to 128×64 pixels.
- Applies binary thresholding.
- Packs every eight pixels into one byte.
- Exports all frames as a C header file (`finalframes.h`).

Each frame occupies

```
128 × 64 pixels

8192 bits

1024 bytes
```

The generated header is then included directly into the Arduino sketch.

---

## Stage 2 — Playback

The ESP32

- Reads bitmap data stored in flash memory.
- Displays one frame at a time.
- Refreshes the OLED approximately every 33 ms.
- Repeats until all frames have been displayed.

---

# Why not simply play an MP4?

A common question is why the project doesn't simply load the MP4 from a computer.

The answer is that the ESP32 is **not a video decoder**.

MP4 files contain compressed H.264 or MPEG video streams which require significant processing power to decode.

The SSD1306 OLED is also extremely limited:

- Resolution: 128×64 pixels
- Monochrome only
- No video controller
- No framebuffer memory
- Communicates over I²C

Unlike a computer monitor, the display has no understanding of image formats or video codecs. It only receives individual pixels.

Therefore every frame must already exist as raw bitmap data before it can be displayed.

---

# Why use `finalframes.h`?

Initially the goal was to stream the video directly from a PC.

However, once the ESP32 is running, it has **no direct access to files stored on a computer**.

It cannot open files such as

```
C:\Users\Username\Videos\video.mp4
```

because those files exist only on the host operating system.

Possible alternatives include

- USB serial streaming
- Wi-Fi streaming
- SD card playback
- SPIFFS filesystem

For this project, storing all frames in program memory was chosen because it

- keeps the project self-contained,
- requires no additional storage hardware,
- allows standalone playback after programming.

---

# Memory Considerations

Each frame requires

```
128 × 64

=

8192 pixels

=

1024 bytes
```

For a 329-frame animation

```
329 × 1024

≈ 336 KB
```

This occupies a significant portion of the ESP32's flash memory but is still practical for relatively short animations.

The data is stored using

```cpp
PROGMEM
```

which places it in flash instead of RAM.

Without PROGMEM the ESP32 would immediately run out of available memory.

---

# Technical Challenges

## 1. OLED Resolution

The original video contains significantly more pixels than the display can show.

Every frame had to be resized to

```
128 × 64
```

which inevitably removes detail.

---

## 2. Monochrome Display

The SSD1306 supports only black and white pixels.

All colour information had to be discarded.

Frames are converted

```
Colour

↓

Grayscale

↓

Binary Threshold

↓

1-bit bitmap
```

---

## 3. Memory Constraints

Unlike a desktop computer, an ESP32 has limited RAM.

Large arrays cannot be stored in RAM.

Using

```cpp
PROGMEM
```

stores the animation in flash memory instead.

---

## 4. Bit Packing

Instead of storing each pixel as one byte,

```
0
1
0
1
...
```

eight pixels are packed into a single byte.

This reduces storage by a factor of eight.

---

## 5. Display Bandwidth

The OLED communicates over I²C, which is relatively slow compared to modern display interfaces.

Large frame sizes or high frame rates quickly become bandwidth-limited.

---

## 6. Binary Header Generation

The Python converter originally produced raw binary data.

Arduino cannot compile raw binary files.

The converter was modified to generate a valid C/C++ header containing

```cpp
const uint8_t videoFrames[] PROGMEM
```

which can be compiled directly into the firmware.

---

# Design Decisions

This implementation prioritises

- simplicity,
- reproducibility,
- minimal hardware,
- standalone operation.

Alternative implementations could use

- SPIFFS
- LittleFS
- SD cards
- external PSRAM
- Wi-Fi frame streaming
- image compression

to support longer videos.

---

# Possible Improvements

- Floyd–Steinberg dithering
- Adaptive thresholding
- GIF support
- Frame compression
- SD card playback
- SPIFFS storage
- Adjustable playback speed
- Wi-Fi streaming
- DMA-driven display updates

---

# Lessons Learned

This project provided experience with

- Computer vision using OpenCV
- Image processing
- Binary image representation
- Bit packing
- Memory optimisation
- Embedded systems programming
- ESP32 development
- SSD1306 graphics programming
- Python and Arduino integration
- Flash memory management

---

# License

MIT License
