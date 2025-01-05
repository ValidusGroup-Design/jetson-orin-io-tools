MIT License

Copyright (c) 2025 Fred Fisher, Validus Group Inc (www.validusgroup.com)

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




import smbus2 as smbus
import time

# Initialize the I2C bus and the sensor address
BUS = 1
ADDRESS = 0x38
bus = smbus.SMBus(BUS)


def read_ath10():
    try:
        # Trigger a measurement (Command 0xAC)
        bus.write_byte(ADDRESS, 0xAC)
        time.sleep(0.1)  # Allow time for measurement

        # Read 6 bytes of data
        data = bus.read_i2c_block_data(ADDRESS, 0x00, 6)

        # Validate status byte: Bit 7 indicates readiness
        if data[0] & 0x80:
            raise ValueError("Sensor not ready")

        # Extract raw humidity and temperature data
        raw_humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        # Scale values according to the datasheet
        humidity = (raw_humidity / (1 << 20)) * 100.0
        temperature = ((raw_temperature / (1 << 20)) * 200.0) - 50.0

        # Convert temperature to Fahrenheit
        temperature_f = (temperature * 9 / 5) + 32

        return round(humidity, 1), round(temperature_f, 1)

    except Exception as e:
        print(f"Error reading sensor: {e}")
        return None, None


if __name__ == "__main__":
    while True:
        humidity, temperature_f = read_ath10()
        if humidity is not None and temperature_f is not None:
            print(f"Humidity: {humidity:.1f}% | Temperature: {temperature_f:.1f}°F")
        else:
            print("Failed to read sensor data.")
        time.sleep(2)
