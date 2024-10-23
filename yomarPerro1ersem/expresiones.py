# eyes
import machine
from machine import Pin, I2C, PWM
import ssd1306
from time import sleep
import gfx
import random
from wifi_and_ntp import *
try:
  import usocket as socket
except:
  import socket
from uselect import select

push_button = Pin(13, Pin.IN) # entrada del boton
maxtime=30 # tiempo maximo de sonido de la alarma

html = """HTTP/1.1 200 OK
Content-Type: text/html
<!DOCTYPE html>
<html>
    <head> <title>MILO Server</title> </head>
    <body>
        <h1>Funciona</h1>
    </body>
</html>
"""

servoPin = PWM(Pin(26),freq=50,duty=77)
origen=100
# ESP32 Pin assignment
i2c = I2C(-1,scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

screen1_row3= "Bienvenido"

screen1 = [[0, 32, screen1_row3]]

graphics = gfx.GFX(oled_width, oled_height, oled.pixel)

ancho_izq=25
ancho_der=25
alto_izq=35
alto_der=35
separacion=4
py_ojos=20
px_izq=int(oled_width/2-ancho_izq-separacion)
px_der=int(oled_width/2+separacion)

sleep_time=1

vidas=5

def synctime():
    txttime=sync_ntp_time()
    oled.text(txttime, 0, 1)

def servo(degrees):
    degrees=degrees+origen
    # limit degrees beteen 0 and 180
    if degrees > origen+20: degrees=origen+20
    if degrees < origen-20: degrees=origen-20
    # set max and min duty
    maxDuty=110
    minDuty=16
    # new duty is between min and max duty in proportion to its value
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    # servo PWM value is set
    servoPin.duty(int(newDuty))
    
def scroll_in_screen(screen):
  for i in range (0, oled_width+1, 4):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)

def scroll_out_screen(speed):
  for i in range ((oled_width+1)/speed):
    for j in range (oled_height):
      oled.pixel(i, j, 0)
    oled.scroll(speed,0)
    oled.show()
    
def limpiar_azul():
    graphics.fill_rect(0, 16, 128, 48, 0)
    
def draweyes(movx=0,movy=0,altoi=0,altod=0,pxi=0,pyi=0,pxd=0,pyd=0,sacada=True,show=True):
    if(sacada and random.randint(0,5)==2):
        movx=movx+random.randint(-1,1)
        movy=movy+random.randint(-1,1)
    limpiar_azul()
    graphics.fill_rect(int(px_izq+movx+pxi), int(py_ojos+movy+pyi), ancho_izq, int(alto_izq+altoi), 1)
    graphics.fill_rect(int(px_der+movx+pxd), int(py_ojos+movy+pyd), ancho_der, int(alto_der+altod), 1)
    if(show):
        oled.show()

def pestaneo():
    draweyes(altoi=-34,altod=-34,pyi=17,pyd=17)
    draweyes()

def guinoi():
    draweyes(altoi=-34,pyi=17)
    draweyes()

def guinod():
    draweyes(altod=-34,pyd=17)
    draweyes()

def cejai(num=1):
    for x in range(num):
        servo(-10)
        draweyes(altoi=-10,pyi=7)
        machine.sleep(sleep_time)
        servo(0)

def cejad(num=1):
    for x in range(num):
        servo(+10)
        draweyes(altod=-10,pyd=7)
        machine.sleep(sleep_time)
        servo(0)

def mirai(num=1):
    servo(-10)
    draweyes(altoi=-1,pyi=1,pxi=-5,pxd=-5)
    draweyes(altoi=-2,pyi=2,pxi=-10,pxd=-10)
    for x in range(num):
        draweyes(altoi=-3,pyi=2,pxi=-15,pxd=-15)
        machine.sleep(sleep_time)
    draweyes(altoi=-2,pyi=2,pxi=-10,pxd=-10)
    draweyes(altoi=-1,pyi=1,pxi=-5,pxd=-5)
    draweyes()
    servo(0)

def mirad(num=1):
    servo(+10)
    draweyes(altod=-1,pyd=1,pxi=5,pxd=5)
    draweyes(altod=-2,pyd=2,pxi=10,pxd=10)
    for x in range(num):
        draweyes(altod=-3,pyd=2,pxi=15,pxd=15)
        machine.sleep(sleep_time)
    draweyes(altod=-2,pyd=2,pxi=10,pxd=10)
    draweyes(altod=-1,pyd=1,pxi=5,pxd=5)
    draweyes()
    servo(0)

def feliz():
    draweyes(altod=-34,altoi=-34,pyi=0,pyd=0,show=False,sacada=False)
    
#lineas por encima     
    graphics.line(int(px_izq+2), int(py_ojos-1), int(px_izq+23), int(py_ojos-1), 1)
    graphics.line(int(px_der+2), int(py_ojos-1), int(px_der+23), int(py_ojos-1), 1)
    
    graphics.line(int(px_izq+3), int(py_ojos-2), int(px_izq+22), int(py_ojos-2), 1)
    graphics.line(int(px_der+3), int(py_ojos-2), int(px_der+22), int(py_ojos-2), 1)
    
    graphics.line(int(px_izq+5), int(py_ojos-3), int(px_izq+20), int(py_ojos-3), 1)
    graphics.line(int(px_der+5), int(py_ojos-3), int(px_der+20), int(py_ojos-3), 1)
    

#lineas abajo
    graphics.line(int(px_izq-1), int(py_ojos+1), int(px_izq+3), int(py_ojos+1), 1)
    graphics.line(int(px_der-1), int(py_ojos+1), int(px_der+3), int(py_ojos+1), 1)
    
    graphics.line(int(px_izq+22), int(py_ojos+1), int(px_izq+26), int(py_ojos+1), 1)
    graphics.line(int(px_der+22), int(py_ojos+1), int(px_der+26), int(py_ojos+1), 1)
    
    
    graphics.line(int(px_izq-2), int(py_ojos+2), int(px_izq+2), int(py_ojos+2), 1)
    graphics.line(int(px_der-2), int(py_ojos+2), int(px_der+2), int(py_ojos+2), 1)
    
    graphics.line(int(px_izq+23), int(py_ojos+2), int(px_izq+27), int(py_ojos+2), 1)
    graphics.line(int(px_der+23), int(py_ojos+2), int(px_der+27), int(py_ojos+2), 1)
    
#texto
    
    oled.show()
    c=3
    while c>0:
        for degree in range(-10,10,1):
            servo(degree)
            sleep(0.01)
    
        for degree in range(10, -10, -1):
            servo(degree)
            sleep(0.01)
        c=c-1
    servo(-20)
    
    

def triste ():
    draweyes(altod=-30,altoi=-30,pyi=0,pyd=0,show=False,sacada=False)
#lineas arriba
    graphics.line(int(px_izq+2), int(py_ojos-1), int(px_izq+24), int(py_ojos-1), 1)
    graphics.line(int(px_der+0), int(py_ojos-1), int(px_der+23), int(py_ojos-1), 1)
    
    graphics.line(int(px_izq+11), int(py_ojos-2), int(px_izq+24), int(py_ojos-2), 1)
    graphics.line(int(px_der+0), int(py_ojos-2), int(px_der+14), int(py_ojos-2), 1)
    
    graphics.line(int(px_izq+14), int(py_ojos-3), int(px_izq+24), int(py_ojos-3), 1)
    graphics.line(int(px_der+0), int(py_ojos-3), int(px_der+11), int(py_ojos-3), 1)
    
    graphics.line(int(px_izq+18), int(py_ojos-4), int(px_izq+24), int(py_ojos-4), 1)
    graphics.line(int(px_der+0), int(py_ojos-4), int(px_der+7), int(py_ojos-4), 1)
        
    oled.show()
    sleep(1)

def enojado():
    draweyes(altod=-30,altoi=-30,pyi=0,pyd=0,show=False,sacada=False)
    
    graphics.line(int(px_izq+0), int(py_ojos-4), int(px_izq+7), int(py_ojos-4), 1)
    graphics.line(int(px_der+18), int(py_ojos-4), int(px_der+25), int(py_ojos-4), 1)
    
    graphics.line(int(px_izq+0), int(py_ojos-3), int(px_izq+11), int(py_ojos-3), 1)
    graphics.line(int(px_der+14), int(py_ojos-3), int(px_der+25), int(py_ojos-3), 1)
    
    graphics.line(int(px_izq+0), int(py_ojos-2), int(px_izq+15), int(py_ojos-2), 1)
    graphics.line(int(px_der+10), int(py_ojos-2), int(px_der+25), int(py_ojos-2), 1)
    
    graphics.line(int(px_izq+0), int(py_ojos-1), int(px_izq+20), int(py_ojos-1), 1)
    graphics.line(int(px_der+5), int(py_ojos-1), int(px_der+25), int(py_ojos-1), 1)
    
    oled.show()
    c=3
    while c>0:
        for degree in range(-10,10,1):
            servo(degree)
            sleep(0.03)
    
        for degree in range(10, -10, -1):
            servo(degree)
            sleep(0.03)
        c=c-1
    servo(1)
    servo(2)
    
def ModoEstudio ():
    graphics.line(int(px_izq+5), int(py_ojos-18), int(px_izq+50), int(py_ojos-18), 1)
    graphics.line(int(px_izq+5), int(py_ojos-18), int(px_izq+5), int(py_ojos+28), 1)
    
    graphics.line(int(px_izq+5), int(py_ojos+28), int(px_izq+50), int(py_ojos+28), 1)
    graphics.line(int(px_izq+50), int(py_ojos+28), int(px_izq+50), int(py_ojos-18), 1)
  
    graphics.line(int(px_izq+8), int(py_ojos-15), int(px_izq+8), int(py_ojos+25), 1)
    graphics.line(int(px_izq+12), int(py_ojos+38), int(px_izq+57), int(py_ojos+38), 1)
    
    graphics.line(int(px_izq+57), int(py_ojos+38), int(px_izq+57), int(py_ojos-8), 1)
#diagonales
    graphics.line(int(px_izq+5), int(py_ojos+28), int(px_izq+12), int(py_ojos+38), 1)
    graphics.line(int(px_izq+50), int(py_ojos+28), int(px_izq+57), int(py_ojos+38), 1)
    
    graphics.line(int(px_izq+50), int(py_ojos-18), int(px_izq+57), int(py_ojos-8), 1)

#paginas
    graphics.line(int(px_izq+55), int(py_ojos+36), int(px_izq+55), int(py_ojos-9), 1)
    graphics.line(int(px_izq+52), int(py_ojos+32), int(px_izq+52), int(py_ojos-15), 1)
    
    graphics.line(int(px_izq+10), int(py_ojos+35), int(px_izq+55), int(py_ojos+35), 1)
    graphics.line(int(px_izq+8), int(py_ojos+32), int(px_izq+51), int(py_ojos+32), 1)
    oled.show()
def inicio():
    draweyes()
    sleep(2)
    feliz()
    sleep(2)
    while True:
          scroll_in_screen(screen1)
          sleep(2)
          scroll_out_screen(4)
          break

def corazones():
    global vidas
    graphics.fill_rect(0, 0, 128, 15, 0)
    for p in range(vidas):
        y=0
        x=p*9
        graphics.line(x+1,y,x+1,y,1);
        graphics.line(x+6,y,x+6,y,1);
        graphics.line(x, y+1, x+2, y+1, 1)
        graphics.line(x+5, y+1, x+7, y+1, 1)
        graphics.line(x, y+2, x+7, y+2, 1)
        graphics.line(x, y+3, x+7, y+3, 1)
        for z in range(4):
            graphics.line(x+z, y+4+z, x+7-z, y+4+z, 1)
    oled.show()
    
def movimientorandom():
    servo(0)
    draweyes()
    if(random.randint(0,5)==2):
        pestaneo()
    if(random.randint(0,5)==2):
        feliz()
    if(random.randint(0,5)==2):
        guinoi()
    if(random.randint(0,5)==2):
        guinod()
    if(random.randint(0,5)==2):
        mirai(4)
    if(random.randint(0,5)==2):
        mirad(4)
    if(random.randint(0,5)==2):
        cejai(4)
    if(random.randint(0,5)==2):
        cejad(4)
    if(random.randint(0,5)==2):
        triste()
    if(random.randint(0,5)==2):
        enojado()

def alarma():
    beeper = PWM(Pin(12, Pin.OUT), freq=2, duty=512) 
    t=time.time()
    while True and (time.time()-t)<maxtime:
        logic_state = push_button.value()
        if logic_state == True:
            break;
    beeper.deinit()
# cliente servidor web

def urldecode(str):
    dic = {"%21":"!","%22":'"',"%23":"#","%24":"$","%26":"&","%27":"'","%28":"(","%29":")","%2A":"*","%2B":"+","%2C":",","%2F":"/","%3A":":","%3B":";","%3D":"=","%3F":"?","%40":"@","%5B":"[","%5D":"]","%7B":"{","%7D":"}"}
    for k,v in dic.items(): str=str.replace(k,v)
    return str

def client_handler(client):
    global html, vidas
    request = client.recv(2048)
    request = str(request)
    response = html
    client.send(response)
    client.close()
    print('Content = %s' % str(request))
    if(request.find("favicon")>0):
        request=""
    # busca vidas
    pv=request.find("?vidas=");
    if(pv>0):
        pf=request[pv+7:pv+8]
        print("Vidas recibidas:"+pf)
        vidrec=int(pf);
        reaccion=0;
        if(vidrec<vidas):
            reaccion=1
        if(vidrec>vidas):
            reaccion=2
        vidas=vidrec
        corazones()
        if(reaccion==1):
            enojado()
        if(reaccion==2):
            feliz()
    # busca alarma
    pv=request.find("?alarma=");
    if(pv>0):
        print("Alarma")
        alarma()
        feliz()
    servo(0)
    
servo(0)
startup()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
inicio()
corazones()
draweyes()

'''
addr = usocket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = usocket.socket()
# s.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
'''



trandom=time.ticks_ms()
while 1:
    r, w, err = select((s,), (), (), 1)
    if r:
        print("conexion")
        for readable in r:
            print("cliente conectado")
            cl, addr = s.accept()
            try:
                client_handler(cl)
            except OSError as e:
                pass
    if(time.ticks_ms()-trandom>=7000):
        print("movimiento random")
        movimientorandom()
        trandom=time.ticks_ms()