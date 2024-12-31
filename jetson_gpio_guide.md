
# Jetson.GPIO Installation and Usage Guide

This guide provides a comprehensive overview of installing and using the `Jetson.GPIO` library on NVIDIA Jetson devices. It covers both system-wide installation and installation within a virtual environment. It also addresses known issues when running in specific development environments like PyCharm.

---

## Prerequisites
Ensure your system meets the following requirements before proceeding:

- NVIDIA Jetson platform with JetPack SDK (4.2 or later)
- Python 3.x installed on your Jetson device

---

## Installation

### System-Wide Installation
System-wide installation is recommended for most users as it simplifies access to GPIO functionality. Follow these steps:

```bash
# Update the system packages
sudo apt update
sudo apt upgrade

# Install Python development tools
sudo apt install python3-dev python3-pip

# Install Jetson.GPIO globally
sudo pip3 install Jetson.GPIO

# Add the current user to the GPIO group for non-root access
sudo groupadd -f gpio
sudo usermod -aG gpio $USER
sudo chmod 770 /dev/gpiochip*

# Log out and log back in to apply group changes
```

To verify the installation:

```bash
python3 -c "import Jetson.GPIO as GPIO; print(GPIO.VERSION)"
```

### Installation in a Virtual Environment (venv)
For projects requiring isolated environments, install `Jetson.GPIO` within a virtual environment. This approach does not require GPIO permissions but is less practical for hardware access in production.

```bash
# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install Jetson.GPIO in the virtual environment
pip install Jetson.GPIO

# Verify the installation
python -c "import Jetson.GPIO as GPIO; print(GPIO.VERSION)"

# To deactivate the virtual environment
deactivate
```

---

## Usage

### Basic Example
Below is a simple example demonstrating how to toggle a GPIO pin.

```python
import Jetson.GPIO as GPIO
import time

# Pin Definitions
output_pin = 12  # BCM pin number

# Pin Setup
GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme
GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)

print("Press CTRL+C to exit")
try:
    while True:
        GPIO.output(output_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(output_pin, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
```

Save the above script and run it using:

```bash
python3 your_script.py
```

---

## Known Issues

### CTRL+C Behavior in PyCharm Terminal
When running `Jetson.GPIO` scripts in the PyCharm terminal, `CTRL+C` may not work to interrupt the program. This is a known limitation of PyCharm's terminal. Use one of the following workarounds:

1. Run the script from a standard terminal where `CTRL+C` works as expected.
2. Use PyCharm's "Stop" button to terminate the running script.

---

## Tips and Best Practices

1. **Root Permissions**:
   - For system-wide installations, you must configure permissions for `/dev/gpiochip*` to avoid running scripts with `sudo`.

2. **Virtual Environment Isolation**:
   - Use a virtual environment when working on multiple projects to avoid dependency conflicts.

3. **Pin Configuration**:
   - Always call `GPIO.cleanup()` in a `finally` block to reset GPIO pins and avoid unintended behavior.

4. **Documentation**:
   - Refer to the [Jetson.GPIO GitHub repository](https://github.com/NVIDIA/jetson-gpio) for additional details and examples.

---

## Troubleshooting

### Module Not Found Error
If you encounter `ModuleNotFoundError: No module named 'Jetson'`, ensure the library is installed in the correct Python environment. Reinstall it using:

```bash
sudo pip3 install --force-reinstall Jetson.GPIO
```

### Permission Denied Errors
Ensure your user has been added to the `gpio` group and that permissions are set correctly on `/dev/gpiochip*`.

```bash
sudo chmod 770 /dev/gpiochip*
```

Log out and log back in to apply changes.

---

For further assistance, please refer to the official documentation or contact the project maintainer.
