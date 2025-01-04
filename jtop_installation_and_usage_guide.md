Installing and Using jtop on NVIDIA Jetson Orin Nano
============================================================================

Overview
--------

`jtop` is a system monitoring tool tailored for NVIDIA Jetson devices.
It provides real-time monitoring of CPU, GPU, memory usage, and other
performance metrics. This guide will walk you through installing and
using `jtop` on the NVIDIA Jetson Orin Nano.

Prerequisites
-------------

-   **JetPack Installed**: Your Jetson Orin Nano should have JetPack
    installed.
-   **Python3 Installed**: `jtop` requires Python 3.x.
-   **Internet Access**: For downloading required packages.

Step 1: Install the Required Dependencies
-----------------------------------------

Open a terminal on your Jetson Orin Nano and run the following commands
to update the system and install necessary dependencies:

    sudo apt update && sudo apt upgrade -y
    sudo apt install python3-pip -y
        

Step 2: Install `jetson-stats`
------------------------------

The `jtop` utility is part of the `jetson-stats` package. Install it
using `pip`:

    pip3 install jetson-stats
        

Verify the installation:

    jtop --version
        

You should see the installed version of `jtop`.

Step 3: Grant Permissions for User Access
-----------------------------------------

To allow non-root users to run `jtop`, add your user to the `video`
group:

    sudo usermod -aG video $USER
        

Log out and log back in for the changes to take effect.

Step 4: Launching `jtop`
------------------------

Run `jtop` from the terminal:

    jtop
        

This command opens an interactive interface displaying real-time system
monitoring data.

Navigating `jtop`
-----------------

-   **CPU and GPU Usage**: View the CPU and GPU utilization on the main
    dashboard.
-   **Temperature Monitoring**: Check real-time temperature readings of
    your Jetson device.
-   **Memory and Disk Usage**: Monitor RAM and storage usage.
-   **Processes**: Inspect currently running processes and their
    resource consumption.

Use the arrow keys to navigate and press `Enter` for more details about
a selected component.

Step 5: Customizing `jtop`
--------------------------

`jtop` allows customization of its dashboard to focus on metrics
important to you. Use the following keys:

-   `t`: Toggle display of temperature.
-   `r`: Refresh data.
-   `q`: Quit `jtop`.

Step 6: Updating `jetson-stats`
-------------------------------

Regular updates to `jetson-stats` ensure compatibility with the latest
JetPack versions. Update using:

    pip3 install --upgrade jetson-stats
        

Troubleshooting
---------------

### `jtop` Command Not Found

Ensure `jetson-stats` is installed correctly. Reinstall using:

    pip3 install --force-reinstall jetson-stats
        

### Permission Issues

Double-check that your user is part of the `video` group:

    groups $USER
        

Conclusion
----------

With `jtop`, you can efficiently monitor and optimize the performance of
your NVIDIA Jetson Orin Nano. For more details and advanced features,
refer to the [official
documentation](https://github.com/rbonghi/jetson_stats).

© 2025 Validus Group Inc. All rights reserved. Unauthorized duplication
or distribution of this material is strictly prohibited.
