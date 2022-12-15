{\rtf1}

This project is based on the Raspberry Pi Pico using CircuitPython libraries

To install, copy the files in the code directory to the mounted Pico 


The design has the RP2040 connected to a Adafruit UDA1334A breakout board using I2S fpr the audio. Code has the pinouts for connecting.
To detect changes of angle of the head mounted sensor, a Adafruit LIS3DH 3 axis accelerometer breakout was used. The one with the Qwicc connector was used.

The output of the UDA1334A is piped into a cheap 5v amplifier from Amazom. Easier version 2 design would be to ause the Adafruit Max98357A breakout which would combine the i2s codec and amp.

There are 2 potentiometers, one for volume that is connected between the UDA1334A and the amplifier. The second is read by the rp2040 to allow changing the sensitivity of the accelerometer.

Used two 1 inch lighed buttons, one selects the sound group and the other toggles between single trigger of sounds and repeated play of the sounds. The lights give feedbaack to button presses.