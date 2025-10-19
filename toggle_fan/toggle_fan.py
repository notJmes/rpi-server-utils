import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(14, GPIO.OUT)
current = GPIO.input(14)

if current:
    GPIO.output(14,GPIO.LOW)
else:
    GPIO.output(14,GPIO.HIGH)
