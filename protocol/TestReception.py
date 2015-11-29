from xmodem import XMODEM
import serial

port = serial.Serial("COM7",baudrate=115200)

#print("envio NACK")
bytesAck = [0x15]
s = "".join(map(chr, bytesAck))
port.write(s)
	
while True:
	#print("espero trama")
	r = port.read()
	#print("llego")
	#print(r)
	#print("envio ACK")
	bytesAck = [6]
	s = "".join(map(chr, bytesAck))
	port.write(s)