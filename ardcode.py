# Importing Libraries
import serial
import time
arduino = serial.Serial( 'COM4', 9600, timeout=0.05)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data)
    return data
write_read('o')