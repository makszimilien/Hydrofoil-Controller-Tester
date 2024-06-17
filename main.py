import serial
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import array as arr
from printer import Printer

# Test-rig motion control
test_rig = Printer()


def start_measurement_sequence(min_speed, max_speed, step):
    test_rig.send_gcode("G28 X0")
    test_rig.send_gcode("G90")
    for speed in range(min_speed, max_speed, step):
        test_rig.send_gcode(f"G1 X160 F{speed}")
        test_rig.send_gcode(f"G1 X0 F{speed}")


min_speed = int(input("Min speed: "))
max_speed = int(input("Max speed: "))
step = int(input("Step: "))

start_measurement_sequence(min_speed, max_speed, step)

# try:
#     s = serial.Serial("/dev/ttyUSB0", 19200, timeout=1)
#     # If the above line doesn't raise an exception, the port is successfully opened
#     print("Serial port /dev/ttyUSB0 is open.")
# except serial.SerialException:
#     print("Failed to open /dev/ttyUSB0. Trying /dev/ttyUSB1 instead.")
#     try:
#         s = serial.Serial("/dev/ttyUSB1", 19200, timeout=1)
#         print("Serial port /dev/ttyUSB1 is open.")
#     except serial.SerialException:
#         print("Failed to open /dev/ttyUSB1. No available serial ports.")

# number_of_test = int(input('Number of measurements: '))
#
# measurements = np.tile(0, number_of_test)
# pwm_inputs = np.tile(0, number_of_test)
# positions = np.tile(0, number_of_test)
# times = np.tile(0.0, number_of_test)
# setpoint = np.tile(0.0, number_of_test)
#
# for x in range(0, number_of_test):
#     buffer = s.readline().decode('utf-8')
#     if buffer.count(":") == 13:
#         # temp_s = buffer.decode()
#         # temp_s = temp_s.strip("\r\n")
#         # temp = float(temp_s)
#
#         # Split the string into parts
#         parts = buffer.split(':')
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
#         #     ws.write(x + 1, 0, datetime.now(), style1)
#         #     ws.write(x + 1, 1, temp, style2)
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
