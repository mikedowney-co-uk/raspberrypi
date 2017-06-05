#!/usr/bin/python3

# Measure the frequency of a pulse train on a gpio pin
# Python equivalent to using the pigpio freq_counter1.c program

import RPi.GPIO as IO
import time
import numpy as np

pin = 26

IO.setwarnings(False)

IO.setmode(IO.BCM)
IO.setup(pin, IO.IN,pull_up_down=IO.PUD_DOWN)

onTimes = []
offTimes = []
pulseIntervals = []

def measureFrequencies(gpiopin, numToRecord = 100):
    global onTimes,offTimes,pulseIntervals
    lastOn = 0
    lastOff = 0
    for i in range(0,numToRecord):
        channel = IO.wait_for_edge(gpiopin, IO.RISING, timeout=5000)
        if channel is None:
            return
        up = time.time()
        channel = IO.wait_for_edge(gpiopin, IO.FALLING, timeout=5000)
        if channel is None:
            return
        down = time.time()
        if lastOff != 0:
            offTimes.append(up-lastOff)
        if lastOn != 0:
            pulseIntervals.append(up-lastOn)
            onTimes.append(down-up)
        lastOn = up
        lastOff = down

for loop in range(0,10):
        measureFrequencies(pin,50)
        cycleTime = np.mean(pulseIntervals)
        onDuration = np.mean(onTimes)
        offDuration = np.mean(offTimes)

        print("frequency = ",1/cycleTime," Hz")
        print("cycle time = ",cycleTime," s")
        print("Pulse Width = ",onDuration," s")
        print("Pulse Gap = ",offDuration," s")
