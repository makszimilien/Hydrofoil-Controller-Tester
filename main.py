import serial
import matplotlib.pyplot as plt
from printer import Printer
import sys
import threading

test_rig = Printer()
is_finished = False
measurements = []


# Test-rig motion control
def run_measurement_motion_sequence():
    global min_speed, max_speed, step
    test_rig.send_gcode("G28 X0")
    test_rig.send_gcode("G90")
    for speed in range(min_speed, max_speed + 1, step):
        test_rig.send_gcode(f"G1 X145 F{speed}")
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
        s.dtr = False
        s.rts = False
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
        try:
            buffer = serial.readline().decode("utf-8")
        except:
            continue
        items = buffer.split(":")
        measurement = {}

        if items[0] == "input" and len(items) == 14:
            for i in range(0, len(items), 2):
                key = items[i]
                value = items[i + 1]

                try:
                    value = float(value)
                except ValueError:
                    pass

                measurement[key] = value

        if "input" in measurement:
            global measurements
            measurements.append(measurement)


def plot_graph(data):
    inputs = [entry["input"] for entry in data]
    setpoints = [entry["setpoint"] for entry in data]
    outputs = [entry["output"] for entry in data]
    kps = [entry["kp"] for entry in data]
    kis = [entry["ki"] for entry in data]
    kds = [entry["kd"] for entry in data]
    distances = [entry["distance"] * -12 for entry in data]

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(inputs, label="Input")
    ax.plot(outputs, label="Output")
    ax.plot(distances, label="Distance")

    # Set plot title and labels
    ax.set_title("Measurements")
    ax.set_xlabel(f"Index, Setpoint: {setpoints[0]}, Kp: {kps[0]}, Ki: {kis[0]}, Kd: {kds[0]}")
    ax.set_ylabel("Value")

    # Add a legend
    ax.legend()

    # Display the plot
    plt.show()


serial = init_serial(115200)

# min_speed = int(input("Min speed: "))
# max_speed = int(input("Max speed: "))
# step = int(input("Step: "))

min_speed = 5000
max_speed = 5001
step = 1

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
