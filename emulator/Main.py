print("INICIO")

i = input("ingresa tu nombre")
print("tu nombre es:"+str(i))

i = input("ingresa tu apellido")
print("tu apellido es:"+str(i))

	
import pyb

s = pyb.Switch(1)
print(s.switch())

def func(sw):
	print("sw pressed!")
	print(sw)

s.callback(func)

l = pyb.LED(1)
g = pyb.LED(4)
l.off()

print("FIN")


c=0
while True:
	l.on()
	pyb.delay(1000)
	l.off()
	
	pyb.delay(1000)	
	print("hola "+str(c))
	c+=1
	g.intensity(c)
	if c==15:
		c=0