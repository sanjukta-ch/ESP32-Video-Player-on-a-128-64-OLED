import cv2
from pathlib import Path


def extract_and_pack_frames(video_path, output_path, target_width=128, target_height=64):
    """
    Convert a video into an Arduino header file containing
    1-bit 128x64 bitmap frames.
    """

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"Error: Cannot open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video: {total_frames} frames @ {fps:.2f} FPS")

    output_data = bytearray()
    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize
        gray = cv2.resize(
            gray,
            (target_width, target_height),
            interpolation=cv2.INTER_AREA,
        )

        # Threshold to black/white
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        pixels = binary.flatten()

        # Pack 8 pixels into one byte
        for i in range(0, len(pixels), 8):

            byte = 0

            for j in range(8):

                if i + j < len(pixels):

                    if pixels[i + j] > 127:
                        byte |= (1 << (7 - j))

            output_data.append(byte)

        frame_count += 1

        if frame_count % 50 == 0:
            print(f"Processed {frame_count}/{total_frames} frames")

    cap.release()

    frame_size = target_width * target_height // 8

    ###########################################################
    # CREATE VALID ARDUINO HEADER
    ###########################################################

    with open(output_path, "w") as f:

        f.write("#pragma once\n")
        f.write("#include <Arduino.h>\n\n")

        f.write(f"#define FRAME_WIDTH {target_width}\n")
        f.write(f"#define FRAME_HEIGHT {target_height}\n")
        f.write(f"#define FRAME_SIZE {frame_size}\n")
        f.write(f"#define FRAME_COUNT {frame_count}\n\n")

        f.write("const uint8_t videoFrames[] PROGMEM = {\n")

        for i, value in enumerate(output_data):

            if i % 16 == 0:
                f.write("    ")

            f.write(f"0x{value:02X}")

            if i != len(output_data) - 1:
                f.write(", ")

            if i % 16 == 15:
                f.write("\n")

        f.write("\n};\n")

    print("\nDone!")
    print(f"Frames      : {frame_count}")
    print(f"Frame Size  : {frame_size} bytes")
    print(f"Total Bytes : {len(output_data)}")
    print(f"Output File : {output_path}")


if __name__ == "__main__":

    video_path = Path(r"video path here")

    output_path = Path(r"path of file you want to create here")  # make sure to add a frames.h name to the file at the end of folder path

    extract_and_pack_frames(video_path, output_path)
