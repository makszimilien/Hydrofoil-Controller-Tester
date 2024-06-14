import serial
from datetime import datetime
import xlwt
import matplotlib.pyplot as plt
import numpy as np
import array as arr

# port = str(input('Add meg a portot (pl.:COM5): '))

try:
    s = serial.Serial("/dev/ttyUSB0", 19200, timeout=1)
    # If the above line doesn't raise an exception, the port is successfully opened
    print("Serial port /dev/ttyUSB0 is open.")
except serial.SerialException:
    print("Failed to open /dev/ttyUSB0. Trying /dev/ttyUSB1 instead.")
    try:
        s = serial.Serial("/dev/ttyUSB1", 19200, timeout=1)
        print("Serial port /dev/ttyUSB1 is open.")
    except serial.SerialException:
        print("Failed to open /dev/ttyUSB1. No available serial ports.")

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0

style1 = xlwt.XFStyle()
style1.num_format_str = 'hh-mm-ss'

style2 = xlwt.XFStyle()
style2.num_format_str = '0.00'

wb = xlwt.Workbook()
ws = wb.add_sheet('Temperature')
ws.write(0, 0, 'Ido', style0)
ws.write(0, 1, 'Homerseklet', style0)

testnum = int(input('Add meg a meresek szamat: '))

measurement = np.tile(0, testnum)
input = np.tile(0, testnum)
position = np.tile(0, testnum)
times = np.tile(0.0, testnum)
setpoint = np.tile(0.0, testnum)

for x in range(0, testnum):
    buffer = s.readline().decode('utf-8')
    if buffer.count(":") == 13:
        # temp_s = buffer.decode()
        # temp_s = temp_s.strip("\r\n")
        # temp = float(temp_s)

        # Split the string into parts
        parts = buffer.split(':')

        # Assign each part to a variable
        property_1 = parts[0]
        property_1_value = parts[1]
        property_2 = parts[2]
        property_2_value = parts[3]
        property_3 = parts[4]
        property_3_value = parts[5]
        property_4 = parts[6]
        property_4_value = parts[7]
        property_5 = parts[8]
        property_5_value = parts[9]
        property_6 = parts[10]
        property_6_value = parts[11]
        property_7 = parts[12]
        property_7_value = parts[13]

        print(property_1, "value:", property_1_value)
        print(property_2, "value:", property_2_value)
        print(property_3, "value:", property_3_value)
        print(property_4, "value:", property_4_value)

        #     ws.write(x + 1, 0, datetime.now(), style1)
        #     ws.write(x + 1, 1, temp, style2)

        measurement[x] = property_3_value
        input[x] = float(property_2_value)
        position[x] = float(property_1_value)
        setpoint[x] = float(property_4_value)
        setpoint_val = property_4_value
        p = property_5_value
        i = property_6_value
        d = property_7_value

        times[x] = x

# wb.save('temperature.xls')

# plotting the points
# plt.plot(times, measurement)
plt.plot(times, input)
plt.plot(times, position)
plt.plot(times, setpoint)

# naming the x-axis
plt.xlabel('Set point: ' + setpoint_val + " P: " + p + " I: " + i + " D: " + d)
# naming the y-axis
plt.ylabel('Input, Output, Set point')
# plt.ylabel('Servo Position')

# giving a title to my graph
plt.title('PID control')

# function to show the plot
plt.show()
