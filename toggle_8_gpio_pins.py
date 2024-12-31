"""
MIT License

Copyright (c) 2024 Fred Fisher, Validus Group Inc. (validusgroup.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import Jetson.GPIO as GPIO
import time
import threading
import signal
import sys

# Define the list of pins to toggle (physical pin numbers)
PINS = [7, 29, 31, 11, 36, 16, 18, 13]

# Create an event to handle termination
stop_event = threading.Event()


def signal_handler(sig, frame):
    """Handles termination signals."""
    print("Termination signal received. Exiting...")
    stop_event.set()


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    """Main function to toggle GPIO pins."""
    try:
        # Set up GPIO using physical pin numbering
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PINS, GPIO.OUT, initial=GPIO.LOW)
    except RuntimeError as e:
        print(f"Failed to initialize GPIO pins: {e}")
        print("Please check if you have the necessary permissions or if another process is using the pins.")
        return
    except Exception as e:
        print(f"Unexpected error during GPIO setup: {e}")
        return

    try:
        print(f"Toggling pins: {', '.join(map(str, PINS))}. Press Ctrl+C to exit.")
        while not stop_event.is_set():
            # Turn all pins ON
            GPIO.output(PINS, GPIO.HIGH)
            print("Pins ON")
            time.sleep(1)

            # Turn all pins OFF
            GPIO.output(PINS, GPIO.LOW)
            print("Pins OFF")
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred during GPIO operation: {e}")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings
        print("GPIO cleanup completed.")


if __name__ == "__main__":
    main()
