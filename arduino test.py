import serial

arduino = serial.Serial('com3', 9600)
mode = 1
arduino.write(str(chr(mode)).encode("0"))
for i in range(10):
    print(arduino.readline())
