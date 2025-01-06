# Bit-Banged GPIO Signal Generator for Jetson Orin Nano
# A Python script for generating square wave signals on GPIO pins using bit-banging.
# Configurable frequency and duty cycle, designed for applications like stepper motor control.
# Ideal for low-demand scenarios where precise timing isn't critical.

# Copyright © Fred Fisher, Validus Group Inc. (www.validusgroup.com)

# This project is dual-licensed under the MIT License and GPL v2.
# You may choose either license based on your needs.

# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# GPL v2 License:
# This program is free software; you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import Jetson.GPIO as GPIO
import time

# Pin configuration
OUTPUT_PIN = 7  # GPIO pin for bit-banging output

# Frequency and duty cycle configuration
FREQUENCY = 100  # 100 Hz
DUTY_CYCLE = 50  # 50%

# Calculate timing
period = 1 / FREQUENCY  # Total period in seconds
high_time = period * (DUTY_CYCLE / 100)  # Time for HIGH state
low_time = period * (1 - (DUTY_CYCLE / 100))  # Time for LOW state


def setup():
    # Set up GPIO mode
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)
    print(f"GPIO {OUTPUT_PIN} configured for output.")


def generate_square_wave():
    print(f"Generating {FREQUENCY} Hz square wave with {DUTY_CYCLE}% duty cycle on GPIO {OUTPUT_PIN}.")
    try:
        while True:
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)
            time.sleep(high_time)
            GPIO.output(OUTPUT_PIN, GPIO.LOW)
            time.sleep(low_time)
    except KeyboardInterrupt:
        print("\nCTRL+C detected. Stopping square wave generation.")


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up.")


if __name__ == "__main__":
    setup()
    try:
        generate_square_wave()
    finally:
        cleanup()
