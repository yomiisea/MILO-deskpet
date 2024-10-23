from machine import Pin, PWM
from time import sleep

servoPin = PWM(Pin(26),freq=50,duty=77)
origen=100


def servo(degrees):
    degrees=degrees+origen
    # limit degrees beteen 0 and 180
    if degrees > origen+20: degrees=origen+20
    if degrees < origen-20: degrees=origen-20
    # set max and min duty
    maxDuty=116
    minDuty=16
    # new duty is between min and max duty in proportion to its value
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    # servo PWM value is set
    print("duty -- "+str(int(newDuty)))
    servoPin.duty(int(newDuty))


while True:
  # start increasing loop
  for degree in range(-10,10,1):
    servo(degree)
    sleep(0.01)
    print("increasing -- "+str(degree))
  # start decreasing loop
  for degree in range(10, -10, -1):
    servo(degree)
    sleep(0.01)
    print("decreasing -- "+str(degree))