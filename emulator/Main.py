print("INICIO")

i = input("ingresa tu nombre")
print("tu nombre es:"+str(i))

i = input("ingresa tu apellido")
print("tu apellido es:"+str(i))

c=0
while True:
	pyb.delay(1000)
	print("hola "+str(c))
	c+=1


	
"""
import pyb

s = pyb.Switch(1)
print(s.switch())

def func(sw):
	print("sw pressed!")
	print(sw)

s.callback(func)

l = pyb.LED(1)
l.on()
l.off()

print("FIN")


c=0
while True:
	pyb.delay(1000)
	print("hola "+str(c))
	c+=1
"""
