OLED display management
-----

# Setup

## Dependencies

[**Enable I2C**](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

[**Setup to control the display with Python**](https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/usage?view=all#usage)

Dependencies:
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo pip install RPi.GPIO
sudo apt-get install python-imaging python-smbus
```

Get the lib:
```
sudo apt-get install git
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
```

## Wiring

[Raspberry Pi pinout diagram from pinout.xyz](https://pinout.xyz/)

+ **4-pin I2C breakout**: connect GND, SDA, SCL to the corresponding Raspberry Pi pins here. Connect screen VCC to RPi's 3.3V.
+ **6-pin I2C breakout** / **SPI**: [follow this Adafruit guide instead](https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black)


# Run

*Note:* `sudo` is required to use GPIO.

`sudo python I2C_SSD1306.py`

