#MIT licence

#Copyright 2022 First FRC team 587 Hedgehogs

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import board
import busio
import adafruit_lis3dh
import array
import math
import audiocore
import audiobusio
import neopixel
import audiomp3
from digitalio import DigitalInOut, Direction, Pull
import analogio


#buttons and leds
#gp18 green button1 LED
#ground blue button1 ground for LED
#gp17 purple button1 switch
#gp16 white button1 used for power for switch
button1Switch = DigitalInOut(board.GP17)
button1Switch.direction = Direction.INPUT
button1Switch.pull = Pull.DOWN
button1Power = DigitalInOut(board.GP16)
button1Power.direction = Direction.OUTPUT
button1Power.value = True
button1Led = DigitalInOut(board.GP18)
button1Led.direction = Direction.OUTPUT
button1Led.value = True

#gp13 green button2 LED
#ground blue button2 ground for LED
#gp14 purple button2 switch
#gp15 white button2 used for power for switch
button2Switch = DigitalInOut(board.GP14)
button2Switch.direction = Direction.INPUT
button2Switch.pull = Pull.DOWN
button2Power = DigitalInOut(board.GP15)
button2Power.direction = Direction.OUTPUT
button2Power.value = True
button2Led = DigitalInOut(board.GP13)
button2Led.direction = Direction.OUTPUT
button2Led.value = True

sensitivityKnob = analogio.AnalogIn(board.GP26)
# using this pin to power the pot
sensitivityKnobPower = DigitalInOut(board.GP27)
sensitivityKnobPower.direction = Direction.OUTPUT
sensitivityKnobPower.value = True

num_pixels = 24
pixel = neopixel.NeoPixel(board.GP6, num_pixels)
pixel.brightness = 0.1

tone_volume = 1.0  # Increase this to increase the volume of the tone.
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

# i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
i2c = busio.I2C(board.GP5, board.GP4)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

def get_angle(xaxis, yaxis):
    if xaxis == 0:
        return 0

    deg = math.degrees(math.atan(yaxis / xaxis))
    if x > 0:
        if y < 0:
            return deg + 360
        else:
            return deg
    else:
        if y < 0:
            return deg + 180
        else:
            return deg + 180

def get_tilt(xaxis, yaxis):
    return math.sqrt((xaxis*xaxis) + (yaxis * yaxis))

def create_tone(frequency):
    length = 8000 // frequency
    sine_wave = array.array("h", [0] * length)
    for i in range(length):
        sine_wave[i] = int(
            (math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1)
        )
    return audiocore.RawSample(sine_wave)

def angle_play_tone(ang, lasttone, repeat):
    idx = math.floor(ang/ (360 / len(samples)))
    print("idx = %d" % (idx))
    if lasttone == -1:
        #audio.play(samples[idx], loop=True)
        audio.play(samples[idx], loop=repeat)
    elif lasttone != idx:
        audio.stop()
        return -1
    return idx

def angle_light(ang, tilt, threshold):
    idx = math.floor(ang/(360 / num_pixels))
    pixel.fill( (15, 15, 15))

    if tilt > threshold:
        pixel[(idx+num_pixels-1)%num_pixels] = (0,190,0)
        pixel[idx] = (0, 255, 0)
        pixel[(idx+1)%num_pixels] = (0,190,0)
    elif tilt > (threshold / 2):
        pixel[(idx+num_pixels-1)%num_pixels] = (209,12,181)
        pixel[idx] = (0, 0, 120)
        pixel[(idx+1)%num_pixels] = (209,12,181)
    elif tilt > (threshold / 3):
        pixel[(idx+num_pixels-1)%num_pixels] = (100,60,121)
        pixel[idx] = (0, 0, 60)
        pixel[(idx+1)%num_pixels] = (100,60,121)


def angle_play_wav(ang, lasttone, repeat):
    idx = math.floor(ang/ (360 / len(waves)))
    print("idx = %d" % (idx))
    if lasttone == -1:
        wave_file = open(waves[idx], "rb")
        wav = audiocore.WaveFile(wave_file)
        audio.play(wav, loop=repeat)
    elif lasttone != idx:
        audio.stop()
        return -1
    #else:
    #    if !audio.playing:
    #        return -1
    #print("Done!")
    return idx

def angle_play_mp3(ang, lasttone, mp3s, repeat):
    idx = math.floor(ang/ (360 / len(mp3s)))
    print("idx = %d" % (idx))
    if lasttone == -1:
        mp3 = audiomp3.MP3Decoder(open(mp3s[idx], "rb"))
        audio.play(mp3, loop=repeat)
    elif lasttone != idx:
        audio.stop()
        return -1
    #print("Done!")
    return idx

def get_threshold(val):
    thresh = (val / 3.0) / 65535
    print("sensitivity = %0.3f, threshold = %0.3f " % (val, thresh))
    return thresh

samples = list()
samples.append(create_tone(440))
samples.append(create_tone(494))
samples.append(create_tone(523))
samples.append(create_tone(587))
samples.append(create_tone(659))
samples.append(create_tone(698))
samples.append(create_tone(784))
samples.append(create_tone(880))

#waves = list()
#waves.append("ride.wav")
#waves.append("kick.wav")
#waves.append("snare.wav")
#waves.append("tom.wav")
#waves.append("Start Auto_normalized.wav")
#waves.append("bicycle_bell.wav")
#waves.append("StarWars3.wav")
#waves.append("CantinaBand3.wav")

trumpet_mp3s = list()
trumpet_mp3s.append("trumpet_C.mp3")
trumpet_mp3s.append("trumpet_D.mp3")
trumpet_mp3s.append("trumpet_E.mp3")
trumpet_mp3s.append("trumpet_F.mp3")
trumpet_mp3s.append("trumpet_G.mp3")
trumpet_mp3s.append("trumpet_A.mp3")
trumpet_mp3s.append("trumpet_B.mp3")
trumpet_mp3s.append("trumpet_high_C.mp3")

drum_mp3s = list()
drum_mp3s.append("clap.mp3")
drum_mp3s.append("closed_hat.mp3")
drum_mp3s.append("crash.mp3")
drum_mp3s.append("hi_hat.mp3")
drum_mp3s.append("kick.mp3")
drum_mp3s.append("ride.mp3")
drum_mp3s.append("snare.mp3")
drum_mp3s.append("tom.mp3")

last_tone = -1
threshold = 0.2
sound_group = 2
loop_repeat = False

#mp3 = audiomp3.MP3Decoder(open("slow.mp3", "rb"))
#audio.play(mp3)
#while audio.playing:
#    pass

def checkButtons():
    if button1Switch.value:
        global sound_group
        sound_group = (sound_group+1)%3
        print("Button1 pressed %d" % (sound_group))
        button1Led.value = False
        time.sleep(0.3)
        button1Led.value = True
        time.sleep(0.1)
        button1Led.value = False
        time.sleep(0.1)
        if sound_group >= 1:
            button1Led.value = True
            time.sleep(0.1)
            button1Led.value = False
            time.sleep(0.1)
        if sound_group >= 2:
            button1Led.value = True
            time.sleep(0.1)
            button1Led.value = False
            time.sleep(0.1)
        button1Led.value = True
    if button2Switch.value:
        button2Led.value = False
        time.sleep(0.5)
        button2Led.value = True
        global loop_repeat
        loop_repeat = not loop_repeat
        print("Button2 pressed")

# Loop forever printing accelerometer values
while True:
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs.
    x, y, z = [
        value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]

    x = -x
    degrees = get_angle(x, y)

    tilt = get_tilt(x,y)
    print("x = %0.3f G, y = %0.3f G, z = %0.3f G, degree = %0.3f, tilt = %0.3f" % (x, y, z, degrees, tilt))
    # Small delay to keep things responsive but give time for interrupt processing.

    threshold = get_threshold(sensitivityKnob.value)

    if tilt > threshold:
        if sound_group == 0:
            last_tone = angle_play_tone(degrees, last_tone, True)
        elif sound_group == 1:
            #last_tone = angle_play_wav(degrees, last_tone)
            last_tone = angle_play_mp3(degrees, last_tone, trumpet_mp3s, loop_repeat)
        else:
            #last_tone = angle_play_wav(degrees, last_tone, loop_repeat)
            last_tone = angle_play_mp3(degrees, last_tone, drum_mp3s, loop_repeat)
    else:
        audio.stop()
        last_tone = -1

    angle_light(degrees, tilt, threshold)

    checkButtons()
    time.sleep(0.1)
