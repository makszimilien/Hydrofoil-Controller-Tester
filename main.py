import serial
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import array as arr
from printer import Printer
import sys
import threading
import time

test_rig = Printer()
is_finished = False
measurements = []


# Test-rig motion control
def run_measurement_motion_sequence(min_speed=15000, max_speed=16000, step=1000):
    test_rig.send_gcode("G28 X0")
    test_rig.send_gcode("G90")
    for speed in range(min_speed, max_speed + 1, step):
        test_rig.send_gcode(f"G1 X160 F{speed}")
        test_rig.send_gcode(f"G1 X0 F{speed}")
    test_rig.wait_move()
    global is_finished
    is_finished = True
    return True


def init_serial(baud):
    try:
        s = serial.Serial("/dev/ttyUSB0", baud, timeout=1)
        # If the above line doesn't raise an exception, the port is successfully opened
        print("Serial port /dev/ttyUSB0 is open.")
        return s
    except serial.SerialException:
        print("Failed to open /dev/ttyUSB0. Trying /dev/ttyUSB1 instead.")
        try:
            s = serial.Serial("/dev/ttyUSB1", baud, timeout=1)
            print("Serial port /dev/ttyUSB1 is open.")
            return s
        except serial.SerialException:
            print("Failed to open /dev/ttyUSB1. No available serial ports.")
            sys.exit(1)


def run_measurement():
    while not is_finished:
        global serial
        buffer = serial.readline().decode('utf-8')
        items = buffer.split(':')
        measurement = {}

        if items[0] == "input":
            for i in range(0, len(items), 2):
                key = items[i]
                value = items[i + 1]

                try:
                    value = float(value)
                except ValueError:
                    pass

                measurement[key] = value
        if 'input' in measurement:
            global measurements
            measurements.append(measurement)
    # return measurements


def plot_graph(data):
    inputs = [entry["input"] for entry in data]
    setpoints = [entry['setpoint'] for entry in data]
    outputs = [entry['output'] for entry in data]
    pwms = [entry['pwm'] for entry in data]
    measured = [entry['measured'] for entry in data]
    kps = [entry['kp'] for entry in data]
    kis = [entry['ki'] for entry in data]
    kds = [entry['kd'] for entry in data]
    distances = [entry['distance'] for entry in data]

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(inputs, label='Input')
    ax.plot(setpoints, label='Setpoint')
    ax.plot(outputs, label='Output')
    ax.plot(pwms, label='PWM')
    ax.plot(measured, label='Measured')
    ax.plot(kps, label='KP')
    ax.plot(kis, label='KI')
    ax.plot(kds, label='KD')
    ax.plot(distances, label='Distance')

    # Set plot title and labels
    ax.set_title('Measurements')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')

    # Add a legend
    ax.legend()

    # Display the plot
    plt.show()


serial = init_serial(19200)

# minimum_speed = int(input("Min speed: "))
# maximum_speed = int(input("Max speed: "))
# step_size = int(input("Step: "))

# Create threads
thread1 = threading.Thread(target=run_measurement_motion_sequence)
thread2 = threading.Thread(target=run_measurement)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

plot_graph(measurements)
