import argparse

import RPi.GPIO as GPIO
import time

# BCM 기준 GPIO 번호
relay_pins = [22, 23, 24, 25]
# relay_pins = [15, 16, 18, 22]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 초기 OFF (액티브 로우 릴레이 기준: HIGH=OFF, LOW=ON)
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def all_off():
    for p in relay_pins:
        GPIO.output(p, GPIO.HIGH)


try:
    # 전원 인가 직후 릴레이 보드 안정화 시간
    all_off()
    time.sleep(1)

    while True:
        for idx, pin in enumerate(relay_pins, start=1):
            # 항상 하나만 켜지도록 먼저 전체 OFF
            all_off()
            time.sleep(0.2)

            print(f"CH{idx} ON (GPIO {pin})")
            GPIO.output(pin, GPIO.LOW)   # ON
            time.sleep(2)

            print(f"CH{idx} OFF (GPIO {pin})")
            GPIO.output(pin, GPIO.HIGH)  # OFF
            time.sleep(1)

except KeyboardInterrupt:
    print("종료")
finally:
    all_off()
    GPIO.cleanup()