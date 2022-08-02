# Hypernova Solar CAN-BUS
CAN-BUS Software for the Hypernova Solar car project

## Libraries
### Python
* [logger](https://docs.python.org/3/howto/logging.html)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [python-can 3.3.3](https://python-can.readthedocs.io/en/master/)
* [tkinter](https://docs.python.org/3/library/tkinter.html)
### Arduino
* [MCP_CAN 1.5](https://github.com/coryjfowler/MCP_CAN_lib)
## Concept
![GUI Concept Image](https://user-images.githubusercontent.com/71153497/94322067-6c2bb080-ff5f-11ea-8db7-31932fe6fd47.png)

# Connecting to the Pi
**There will be a better setup in the future, but this is how it currently works.**
## Network Setup
The Pi is currently set up to connect to a Wi-Fi network with the following configuration.

| Property     | Setting       |
|--------------|---------------|
|SSID          | hotspot       |
|Encryption    | WPA2-PSK      |
|Password      | hypernovarox  |
|Band          | 2.4Ghz        |

On Windows, you can set up a mobile hotspot to share your internet connection with other devices. Simply search "Mobile Hotspot" within the settings app and configure the hotspot according to the settings above. (Note: SSID is equivalent to Network Name, and the encryption will be WPA2-PSK by default)

## SSH
Once the Pi connects, you will see it along with its IP in Mobile Hotspot settings. To connect to it you must have the ssh private key file, please message the Hypernova Discord if you do not have it. **Password login over SSH is disabled for security.**

If you have the keyfile and the Pi is connected to your machine, access it using the command.
```
ssh -i <path to keyfile> pi@<IP of Pi>
```

For example, if the IP of the Pi was `192.168.100.20` and the private keyfile was located at `C:\Users\John\hypernova`
```
ssh -i C:\Users\John\hypernova pi@192.168.100.20
```

There will be no SSH password prompt as the keyfile serves as the authentication.

You should now be able to run commands on the Pi.

# Battery Charger
In order to charge the batteries, the BMS must be supplied with the required DC voltage and current. Our batteries are rated at a maximum 4.2 A charging current to charge a cell to a maximum of 4.2 V. For our 20S11P battery pack, the supply must be able to supply 46.2 A at 84 V.

$I = 4.2 A \cdot 11 = 46.2 A$

$V = 4.2 V \cdot 20 = 84 V$

The supply is being designed to supply 50 A at 84 V. Safety measures have not been implemented yet, but will be included in the final design.
