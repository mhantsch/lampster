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

Take that HEX MAC address for Lampster and put it in the `--device` parameter of the `gantttool` calls in the `lampster` script.

## Usage

### lampster

`lampster [-t] [on|off]`

Turn the Lampster on or off.

*Note:* The commands sent by `gatttool` sometimes fail. I don't know why. The script tries them up to 5 times before giving up. If you call it with the `-t` parameter it will tell you about failed tries.

### autolampster

Simple script to monitor your login and logout (actually, screen lock/unlock) and turn the Lampster on whenever you unlock the screen (login), and turn it off whenever you lock the screen (logout). You have to figure out how to automatically run this when the system is on.

## Technical details

### Connect to the Lampster

```
gatttool -I -b XX:XX:XX:XX:XX:XX
connect
```

### Control the Lampster

Once connected use the following commands.

#### Mode selection

| command | description |
| --- | --- |
| char-write-req 0x0021 c0 | turn it on |
| char-write-req 0x0021 40 | turn it off |
| char-write-req 0x0021 a8 | activate RGB mode |
| char-write-req 0x0021 c8 | activate WHITE mode |
| char-write-req 0x0021 28 | activate OFF mode?!? |

#### White LEDs

Once you are in WHITE mode you can adjust the warm white and cold white LEDs with this command:

| command | description |
| --- | --- |
| char-write-cmd 0x0025 WWCC  WW for warm white LEDs, CC for cold white LEDs

The values seem to be Hex and range from 00 to 64 (0 to 100%).
| command | description |
| --- | --- |
| char-write-cmd 0x0025 0100 | lowest warm white intensity |
| char-write-cmd 0x0025 6400 | highest warm white intensity |
| char-write-cmd 0x0025 0001 | lowest cold white intensity |
| char-write-cmd 0x0025 0064 | highest cold white intensity |
| char-write-cmd 0x0025 1E1E | both 30% intensity |
| char-write-cmd 0x0025 6464 | both full intensity |

#### RGB LEDs

Once you are in RGB mode you can adjust the colors with this command:

| command | description |
| --- | --- |
| char-write-cmd 0x002a RRGGBB | RR for red LEDs, GG for green LEDs, BB for blue LEDs |

The values seem to be Hex and range from 00 to 64 (0 to 100%).

| command | description |
| --- | --- |
| char-write-cmd 0x002a 010000 | RED lowest intensity |
| char-write-cmd 0x002a 640000 | RED highest intensity |
| char-write-cmd 0x002a 000100 | GREEN lowest intensity |
| char-write-cmd 0x002a 006400 | GREEN highest intensity |
| char-write-cmd 0x002a 000001 | BLUE lowest intensity |
| char-write-cmd 0x002a 000064 | BLUE highest intensity |
| char-write-cmd 0x002a 1E1E1E | all 30% intensity |
| char-write-cmd 0x002a 646464 | all full intensity |
