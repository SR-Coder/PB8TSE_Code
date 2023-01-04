

from machine import Pin

led = Pin("LED", Pin.OUT)

def toggle():
    led.toggle()


def getValue(pin):
    return pin.value()