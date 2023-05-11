import serial
import matplotlib.pyplot as plt
import threading
import time
import csv
from matplotlib.animation import FuncAnimation

PORT1_NAME = 'COM5'  # Data
PORT2_NAME = 'COM15'  # Picture
BAUD_RATE = 115200

temperature_data = []
humidity_data = []
altitude_data = []
pressure_data = []

FILENAME = 'img'

JPEG_BEGIN = b'\xff\xd8'
JPEG_END = b'\xff\xd9'

byte_stream = b''

ser1 = serial.Serial(PORT1_NAME, BAUD_RATE)  # Data
ser2 = serial.Serial(PORT2_NAME, BAUD_RATE)  # Picture

stream = b''
img_buf = b''
idx = 1
bytes_idx = 0

loop_running = True


def write_buf(filename: str, buf: bytes):
    with open('{}.jpg'.format(filename), mode='wb') as f:
        f.write(buf)


def plot_data():
    global temperature_data, humidity_data, altitude_data, pressure_data

    fig, axs = plt.subplots(2, 2, figsize=(8, 8))

    line1, = axs[0, 0].plot([], [], color='green')
    line2, = axs[0, 1].plot([], [], color='blue')
    line3, = axs[1, 0].plot([], [], color='red')
    line4, = axs[1, 1].plot([], [], color='purple')

    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_ylabel('Temperature (Â°C)')

    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_ylabel('Humidity (%)')

    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_ylabel('Altitude (m)')

    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_ylabel('Pressure (Pa)')

    def update(frame):
        global temperature_data, humidity_data, altitude_data, pressure_data, loop_running

        data = ser1.readline().decode().strip()

        with open('data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data])

        data_split = data.split(",")
        temperature = float(data_split[1])
        humidity = float(data_split[2])
        altitude = float(data_split[3])
        pressure = float(data_split[4])

        temperature_data.append(temperature)
        humidity_data.append(humidity)
        altitude_data.append(altitude)
        pressure_data.append(pressure)

        if len(temperature_data) > 100:
            temperature_data.pop(0)
            humidity_data.pop(0)
            altitude_data.pop(0)
            pressure_data.pop(0)

        line1.set_data(range(len(temperature_data)), temperature_data)
        line2.set_data(range(len(humidity_data)), humidity_data)
        line3.set_data(range(len(altitude_data)), altitude_data)
        line4.set_data(range(len(pressure_data)), pressure_data)

        for ax in axs.ravel():
            ax.relim()
            ax.autoscale_view()

    ani = FuncAnimation(fig, update, interval=100)

    plt.tight_layout()
    plt.show()
    loop_running = False
    # END DATA SAVE

    # BEGIN IMAGE SAVE

def save_images():
    global stream, idx

    while loop_running:
        if ser2.in_waiting > 0:
            stream += ser2.read(ser2.in_waiting)

        start = stream.find(JPEG_BEGIN)
        stop = stream.find(JPEG_END)

        if start > stop:
            stream = stream[stream.rfind(JPEG_BEGIN):]
            print('Invalid start/stop, recapturing...')

        elif -1 < start < stop:
            img_buffer = stream[start:stop + len(JPEG_END)]
            write_buf('./output/{}{}'.format(FILENAME, idx), img_buffer)
            print('\nImage', idx, 'is saved.')
            idx += 1
            stream = b''

        time.sleep(0.5)


image_thread = threading.Thread(target=save_images)
image_thread.start()

plot_data()
image_thread.join()
