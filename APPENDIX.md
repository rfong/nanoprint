# Appendix: Parts list

Note that you can get most any component except the Raspberry Pi for around half price if you’re willing to wait a month for Aliexpress.

## Printer & controller (~$75 / min $60)
+ TTL nano thermal printer ([$45 from Adafruit](https://www.adafruit.com/product/2752) | [$30 from Aliexpress](https://www.aliexpress.com/item/Thermal-Printer-Series-supports-RS232-TTL/1325607965.html))
+ Raspberry Pi Zero W ($10)
    + optional: 2 x 20 header ($1)
    + MicroSD card ($7-$10)
    + shipping costs T_T ($10)
+ 5V 2A microUSB power supply ($7, but you probably already have this)
+ NPN transistor ([$2/10pk](https://www.adafruit.com/product/756))
+ USB micro B female breakout ([$1.50 Adafruit](https://www.adafruit.com/product/1833) | [$3/10pk Amazon](https://www.amazon.com/gp/product/B0183KF7TM))

## Optional interface (~$15 / min $5)
+ OLED screen ([$10 Amazon](https://www.amazon.com/gp/product/B00O2KDQBE) | [$3 Aliexpress](https://www.aliexpress.com/item/0-96-inch-IIC-Serial-White-OLED-Display-Module-128X64-I2C-SSD1306-12864-LCD-Screen-Board/32780054633.html))
    + You have the option of an I2C or SPI interface. SPI is faster, but requires 5 pins besides power, while I2C only requires 2 pins besides power. For my purpose of displaying a simple menu, the performance differences didn’t matter, so I went  with I2C. ([Here’s an electronics.StackExchange post on I2C vs SPI tradeoffs.](https://electronics.stackexchange.com/questions/29037/tradeoffs-when-considering-spi-or-i2c))
+ Piezo buzzer ([$1](https://www.adafruit.com/product/1740))
+ rocker switch ($.50)
+ pushbuttons ($2.50/10pk)
+ assorted resistors
+ wires, protoboard, etc

## Handy extras
+ Enclosure ($0–10)
    I wanted nice hardwood for the final enclosure, but you could easily stop at the cardboard box phase or the free scrap plywood phase, since people throw away lots of 3" scraps while lasercutting that this teeny tiny project can easily fit on.
M2 screws — used to secure my boards to the enclosure, but you can be lazy and hot glue it all if you want.
+ Paper refill — 16'L 2.25"W rolls ([$10/10pk](https://www.amazon.com/dp/B01N7RMC70/))
+ Portable 5V 2A power bank ($11+)
+ micro USB adapter ($2-3) for interfacing with peripherals

## Hidden setup costs
If you haven’t worked on a soldering project before, [Adafruit has a great intro with tool recommendations](https://learn.adafruit.com/adafruit-guide-excellent-soldering/tools)! I benefitted a ton from their solder joint debugging guide while learning how to solder.

Other hidden costs that I already had on hand from previous projects:
+ Soldering setup (soldering iron & solder, helping hand, pliers, wire strippers, desoldering wick)
+ Breadboards, jumper wires (mostly M-M and M-F), LEDs, resistors
+ Protoboard, pushbuttons, hookup wire, heatshrink
+ literally a bag full of microUSB cables & adapters
+ Various woodworking tools & measuring tools



# Appendix: References
Guides referenced:
+ [Preparing an SD card for Raspberry Pi](https://learn.adafruit.com/adafruit-raspberry-pi-lesson-1-preparing-and-sd-card-for-your-raspberry-pi/overview)
+ [Raspberry Pi Zero — SSH setup without adapters](https://davidmaitland.me/2015/12/raspberry-pi-zero-headless-setup/)
+ [Configure I2C on Raspberry Pi](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)
+ [Install printer drivers on Raspberry Pi](https://learn.adafruit.com/instant-camera-using-raspberry-pi-and-thermal-printer/system-setup#install-software)
+ [Thermal printer wiring](https://learn.adafruit.com/instant-camera-using-raspberry-pi-and-thermal-printer/connections#printer)
+ [OLED screen setup](https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/usage?view=all#usage)
+ [Ladyada | Pushbuttons](http://www.ladyada.net/learn/arduino/lesson5.html)
+ [Setting up WiringPi (GPIO interface lib)](http://wiringpi.com/download-and-install/)
