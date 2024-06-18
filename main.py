import serial
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import array as arr
from printer import Printer
import sys
import threading
import time

# Test-rig motion control
test_rig = Printer()
is_finished = False


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
    global s
    try:
        s = serial.Serial("/dev/ttyUSB0", baud, timeout=1)
        # If the above line doesn't raise an exception, the port is successfully opened
        print("Serial port /dev/ttyUSB0 is open.")
    except serial.SerialException:
        print("Failed to open /dev/ttyUSB0. Trying /dev/ttyUSB1 instead.")
        try:
            s = serial.Serial("/dev/ttyUSB1", baud, timeout=1)
            print("Serial port /dev/ttyUSB1 is open.")
        except serial.SerialException:
            print("Failed to open /dev/ttyUSB1. No available serial ports.")
            sys.exit(1)


def run_measurement():
    pid_inputs = np.tile(0, 1)
    pid_outputs = np.tile(0, 1)
    measurements = np.tile(0, 1)
    pwm_inputs = np.tile(0, 1)
    positions = np.tile(0, 1)
    times = np.tile(0.0, 1)
    setpoint = 0
    p = 0.0
    i = 0.0
    d = 0.0

    while not is_finished:
        buffer = s.readline().decode('utf-8')
        sections = buffer.split(':')
        if sections[0] == "input":
            for section in sections:
                print(section)
    #         # temp_s = buffer.decode()
    #         # temp_s = temp_s.strip("\r\n")
    #         # temp = float(temp_s)
    #

    #
    #         # Assign each part to a variable
    #         property_1 = parts[0]
    #         property_1_value = parts[1]
    #         property_2 = parts[2]
    #         property_2_value = parts[3]
    #         property_3 = parts[4]
    #         property_3_value = parts[5]
    #         property_4 = parts[6]
    #         property_4_value = parts[7]
    #         property_5 = parts[8]
    #         property_5_value = parts[9]
    #         property_6 = parts[10]
    #         property_6_value = parts[11]
    #         property_7 = parts[12]
    #         property_7_value = parts[13]
    #
    #         print(property_1, "value:", property_1_value)
    #         print(property_2, "value:", property_2_value)
    #         print(property_3, "value:", property_3_value)
    #         print(property_4, "value:", property_4_value)
    #
    #
    #         measurements[x] = property_3_value
    #         pwm_inputs[x] = float(property_2_value)
    #         positions[x] = float(property_1_value)
    #         setpoint[x] = float(property_4_value)
    #         setpoint_val = property_4_value
    #         p = property_5_value
    #         i = property_6_value
    #         d = property_7_value
    #
    #         times[x] = x
    #
    # # wb.save('temperature.xls')
    #
    # # plotting the points
    # # plt.plot(times, measurement)
    # plt.plot(times, pwm_inputs)
    # plt.plot(times, positions)
    # plt.plot(times, setpoint)
    #
    # # naming the x-axis
    # plt.xlabel('Set point: ' + setpoint_val + " P: " + p + " I: " + i + " D: " + d)
    # # naming the y-axis
    # plt.ylabel('Input, Output, Set point')
    # # plt.y-label('Servo Position')
    #
    # # giving a title to my graph
    # plt.title('PID control')
    #
    # # function to show the plot
    # plt.show()


init_serial(19200)

# minimum_speed = int(input("Min speed: "))
# maximum_speed = int(input("Max speed: "))
# step_size = int(input("Step: "))

# is_finished = run_measurement_sequence(minimum_speed, maximum_speed, step_size)

# Create threads
thread1 = threading.Thread(target=run_measurement_motion_sequence)
thread2 = threading.Thread(target=run_measurement)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

#
