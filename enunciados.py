# import raspberry pi GPIO module
import RPi.GPIO as GPIO
import time

#asignacion de pines de la raspberry a variables
sensor_S=3
sensor_R=5
sensor_D=7
sensor_V=8
actuador_B=10

sensor_G=11
sensor_H=12
sensor_T45=13
sensor_T60=15
alarma_A=18

selector=19 #cambia para circuito de riego o circuito de alarma



# configuracion de pines de entrada de la raspberry 
########## ENUNCIADO 1 #############
GPIO.setup(sensor_S, GPIO.IN)     #S: Señal que indica si la tierra está seca
							#Tierra seca: S=1; Tierra húmeda: S=0

GPIO.setup(sensor_R, GPIO.IN)     #R: Señal que indica si hay restricciones en el riego (es verano)
							#Hay restricciones:R=1 No hay restricciones: R=0

GPIO.setup(sensor_D, GPIO.IN)     #D: Señal que indica si es de día o de noche
							#Día: D=1; Noche: D=0

GPIO.setup(sensor_V, GPIO.IN)	   #V: Señal que indica si el depósito de agua está vacío
							#Vacío: V=1; Hay agua: V=0

GPIO.setup(actuador_B, GPIO.OUT)   #B: que accionará la bomba para regar
							# B=1; Bomba apagada B=0


########## ENUNCIADO 2 #############
GPIO.setup(sensor_G, GPIO.IN)    #G: señal de GAS
							#G: vale '1' si se detecta GAS resultante de la combustión.

GPIO.setup(sensor_H, GPIO.IN)	   #H: señal de HUMO
							#H: vale '1' si se detecta HUMO

GPIO.setup(sensor_T45, GPIO.IN)	   #T45: sensor temperatura T45
							#T45: vale '1' si la temperatura es superior a 45ºC

GPIO.setup(sensor_T60, GPIO.IN)	   #T60: sensor temperatura T60
							#T60: vale '1' si la temperatura es superior a 60ºC

GPIO.setup(alarma_A, GPIO.OUT)   #A: señal de alarma
							#A:  se activará a nivel alto

GPIO.setup(selector, GPIO.IN)    #selector de enunciados 
							#selector:0 enunciado 1    selector:1 enunciado 2


############ ENUNCIADO 1
class riego:
	#atributos
	S=0
	R=0
	D=0
	V=0

	#constructor
	def __init__(self,S,R,D,V):
		self.S=S
		self.R=R
		self.D=D
		self.V=V

	def operacion(self,S,R,D,V):
		
		if V==1: #bomba vacia
			GPIO.output(actuador_B, GPIO.LOW) #bomba apagada
			modo=0

		elif V==0: #hay agua

			if R==1: #hay restricciones
				if D==0: #es de noche
					GPIO.output(actuador_B, GPIO.HIGH) #bomba encendida
					modo=1
				elif D==1: #es de dia
					GPIO.output(actuador_B, GPIO.LOW) #bomba apagada
					modo=2

			elif R==0: #no hay restricciones
				if S==1: #si la tierra esta seca
					GPIO.output(actuador_B, GPIO.HIGH) #bomba encendida
					modo=3
				elif S==0: #si la tierra esta humeda
					GPIO.output(actuador_B, GPIO.LOW) #bomba apagada
					modo=4
		return modo

	def imprimir(self,modo):
		if modo==0:
			print("BOMBA APAGADA: No hay agua")
		elif modo==1:
			print("BOMBA ENCENDIDA: con restriccion")
			print("V=1 Hay agua")
			print("D=0 Es de NOCHE")
		elif modo==2:
			print("BOMBA APAGADA: con restriccion")
			print("V=1 Hay agua")
			print("D=0 Es de DIA")
		elif modo==3:
			print("BOMBA ENCENDIDA: sin restriccion")
			print("V=1 Hay agua")
			print("S=1 Tierra SECA")
		elif modo==4:
			print("BOMBA APAGADA: sin restriccion")
			print("V=1 Hay agua")
			print("S=1 Tierra HUMEDA")




############ ENUNCIADO 2
class circuito:
	#atributos
	G=0
	H=0
	T45=0
	T60=0

	#constructor
	def __init__(self,G,H,T45,T60):
		self.G=G
		self.H=H
		self.T45=T45
		self.T60=T60

	def operacion(self,G,H,T45,T60):
        
		if T60==1: #Temperatura mayor a 60
			GPIO.output(alarma_A, GPIO.HIGH) #alarma activada
			modo=1

		elif T45==1 and T60==0: #Temperatura entre 45 y 60
			if (G==1 or H==1)or(G==1 and H==1): #si han detectado gases o humos (o ambos).
				GPIO.output(alarma_A, GPIO.HIGH) #alarma activada
				modo=2
			else:
				GPIO.output(alarma_A, GPIO.LOW) #alarma desactivada
				modo=0

		elif T45==0 and T60==0: #temperatura menor a 45
			if (G==1 or H==1):
				GPIO.output(alarma_A, GPIO.HIGH) #alarma activada
				modo=3
			else:
				GPIO.output(alarma_A, GPIO.LOW) #alarma desactivada
				modo=0
        
		return modo

	def imprimir(self,modo):
		if modo==0:
			print("Alarma desactivada")
		elif modo==1:
			print("ALARMA ACTIVADA")
			print("T60=1 Temperatura MAYOR a 60 °C")
		elif modo==2:
			print("ALARMA ACTIVADA")
			print("T60=0 y  T45=1 Temperatura en rango de 45-60°C")
			print("Se han detectado gases y/o humos")
		elif modo==3:
                        print("ALARMA ACTIVADA")
			print("T60=0 y  T45=0 Temperatura en rango de 45-60°C")
			print("Se han detectado gases o humos")

#se instancian los objetos de las clases
manguera=riego(0,0,0,0)
incendio=circuito(0,0,0,0)

while (True):
	
	if(GPIO.input(selector)==0):
		mod=manguera.operacion(GPIO.input(sensor_S),GPIO.input(sensor_R),GPIO.input(sensor_D),GPIO.input(sensor_V))
		manguera.imprimir(mod)
		time.sleep(0.25)
		
	elif(GPIO.input(selector)==1):
		mod=incendio.operacion(GPIO.input(sensor_G),GPIO.input(sensor_H),GPIO.input(sensor_T45),GPIO.input(sensor_T60))
		incendio.imprimir(mod)
		time.sleep(0.25)
