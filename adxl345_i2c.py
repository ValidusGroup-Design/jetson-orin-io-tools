# Dual License: MIT and GPLv3
# Copyright (c) 2025 Fred Fisher, Validus Group Inc.
# www.validusgroup.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Alternatively, this software may be redistributed and/or modified under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

import smbus2
import time
import argparse

# Constants for the ADXL345
ADXL345_ADDRESS = 0x53
REG_POWER_CTL = 0x2D
REG_DATA_FORMAT = 0x31
REG_DATAX0 = 0x32

# Scale factor for raw acceleration data
ACCEL_SCALE = 0.004  # 4 mg/LSB assuming +/-2g range

def initialize_adxl345(bus):
    """Initialize the ADXL345 accelerometer."""
    # Wake up the device
    bus.write_byte_data(ADXL345_ADDRESS, REG_POWER_CTL, 0x08)

    # Set data format to +/-2g with full resolution
    bus.write_byte_data(ADXL345_ADDRESS, REG_DATA_FORMAT, 0x08)

def read_acceleration(bus):
    """Read acceleration data from the ADXL345."""
    data = bus.read_i2c_block_data(ADXL345_ADDRESS, REG_DATAX0, 6)

    # Convert the raw data to g units
    x = (data[1] << 8 | data[0]) if data[1] < 128 else ((data[1] << 8 | data[0]) - 65536)
    y = (data[3] << 8 | data[2]) if data[3] < 128 else ((data[3] << 8 | data[2]) - 65536)
    z = (data[5] << 8 | data[4]) if data[5] < 128 else ((data[5] << 8 | data[4]) - 65536)

    return x * ACCEL_SCALE, y * ACCEL_SCALE, z * ACCEL_SCALE

def main():
    parser = argparse.ArgumentParser(description="Read data from ADXL345 on I2C bus 7 at address 0x53.")
    parser.add_argument("--samples", type=int, default=10, help="Number of samples to read")
    parser.add_argument("--interval", type=float, default=0.5, help="Interval between samples in seconds")
    args = parser.parse_args()

    try:
        bus = smbus2.SMBus(7)
        initialize_adxl345(bus)
        print("ADXL345 initialized. Reading data...")

        for _ in range(args.samples):
            x, y, z = read_acceleration(bus)
            print(f"X: {x:.4f} g, Y: {y:.4f} g, Z: {z:.4f} g")
            time.sleep(args.interval)

    except FileNotFoundError:
        print("Error: Could not open I2C bus 7. Ensure the device is connected.")
    except OSError as e:
        print(f"I2C communication error: {e}")
    finally:
        try:
            bus.close()
        except:
            pass

if __name__ == "__main__":
    main()
