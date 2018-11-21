# RPiPWM
Проект для работы с шилдом для компьютера Raspberry PI, 
который предназначен для генерирования 16 каналов ШИМ сигнала.

### Описание
Библиотека содержит классы для работы с однокональным ацп MCP3221, который измеряет напряжение питания,
микросхемой PCA9685, который создает ШИМ сигнал на 16 каналах, для управления светодиодом и кнопкой на плате,
при помощи модуля RPi.GPIO, а также для работы с дисплеем на базе микросхемы SSD1336.  
Пример работы в файле **example.py**.  
Подробное описание функций в файле **Description**.

### Необходимые модули
Стандартные: `time`, `enum`, `math`, `threading`.  
Дополнительные:  
- RPi.GPIO - для работы с GPIO Raspberry Pi  
Устанавливается либо через pip3: `sudo pip3 install RPi.GPIO`, либо через apt: `sudo apt install python3-rpi.gpio`
- smbus - для работы с шиной i2c  
Устанавливается из репозитория: `sudo apt install python3-smbus`

**ВАЖНО:** Для работы примера нужен дополнительный модуль, который не является необходимым для работы библиотеки.  
- PIL - Python Imaging Library - модуль, используемый для создания изображений, которые выводятся на дисплей.  
Устанавливается через pip3: `sudo pip3 install pillow`

### Полезные ссылки
- Даташит для ШИМ контроллера [PCA9685](https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf)
- Даташит для дисплея [SSD1306](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
- Даташит для АЦП [MCP3221](http://ww1.microchip.com/downloads/en/DeviceDoc/20001732E.pdf)
- Даташит для измерителя питания [INA219](http://www.ti.com/lit/ds/symlink/ina219.pdf) (*функционал дорабатывается*)