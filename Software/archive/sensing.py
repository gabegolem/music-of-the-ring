from machine import Pin, ADC, I2C
import time
from lsm6ds3 import LSM6DS3, NORMAL_MODE_104HZ

print("PIEZO TEST")

piezo_pin = Pin(18)
adc = ADC(piezo_pin)

i2c = I2C(0, scl=Pin(4), sda=Pin(3))
print(i2c.scan())
#sensor = LSM6DS3(i2c, mode=NORMAL_MODE_104HZ)

adc.atten(ADC.ATTN_11DB)

threshold = 8000
while True:
    # Read the analog value.
    # For ESP32/Pico, read_u16() returns a 16-bit value (0-65535).
    # For ESP8266, read() returns a 10-bit value (0-1023).
    value = adc.read_u16() 

    if (value > threshold):
        print(f"Analog value: {value}")
    
    # Optional: Map the value to a percentage if needed
    # percentage = (value / 65535) * 100 
    # print(f"Percentage: {percentage:.2f}%")

    time.sleep(0.01) # Wait for 0.5 seconds before the next reading