# Lampster scripts
Some simple bash shell scripts to control my Lampster lamp via Bluetooth.

## Setup
You need to install `bluez` for the bluetooth stack and the `gatttool` command. On my Pop_OS! 22.04 Linux installation on a Laptop with a Bluetooth interface, it was already installed.

Then, find the device id of your lampster
```
bluetoothctl
scan on
exit
```

After `scan on`, you should see something like
```
Discovery started
[CHG] Controller BC:09:1B:F4:DC:87 Discovering: yes
[NEW] Device XX:XX:XX:XX:XX:XX Some other Devices...
[NEW] Device C0:00:00:04:5B:91 Lampster
```

Take that HEX MAC address for Lampster and put it in the `--device` parameter of the `lampster` script.

## Usage

### lampster
`lampster [-t] [on|off]`

Turn the Lampster on or off.

*Note:* The commands sent by `gatttool` sometimes fail. I don't know why. The script tries them up to 5 times before giving up. If you call it with the `-t` parameter it will tell you about failed tries.

### autolampster
Simple script to monitor your login and logout (actually, screen lock/unlock) and turn the Lampster on whenever you unlock the screen (login), and turn it off whenever you lock the screen (logout). You have to figure out how to automatically run this when the system is on.
