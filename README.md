# ELEC-E8408-Hiking-Tour-Assistant
The project consist of Raspberry 3b+ (RPi) and LilyGo TWATCH V2. Database and webUI is ran on RPi and LilyGoWatch gathers hiking session data, and sends it to the database via Bluetooth.
## How to initialize Raspberry Pi support platform for Hiking Tour Asistant:
1. Clone repository to Raspberry Pi.
2. Run "run_script.sh to initialize bluetooth receiver and local webserver in the backround.
```
sh run_script.sh
```
3. Use CTRL+C to stop the associated processes when ready.
4. In case of the database is empty, the webserver has to be ran first, user has to be created to be able to run the receiver.py



## How to initialize the LilyGo smartwatch
1. Clone TWatch repository on Linux-based system
2. Install VSCode and Platformio
3. In Platformio.ini, the required libraries are presented and fetched from github.
4. At the start, the LITTLEFS complains about that it does not get enough parameters which was fixed by giving the function which caused the error an additional parameter (true)
5. Press Upload in VSCode.

##Watch_TTGo_fw libraries
In this project the smartwatch utilizes TTGO-Watch-Library (https://github.com/Xinyuan-LilyGO/TTGO-T-Watch) to enable the functionalities of the watch such as the BMA423 accelerometer. For saving the sessions to Flash memory, LITTLEFS (https://github.com/lorol/LITTLEFS) was enabled.
Arduinos Bluetooth library was used to enable the communication between the RPi and TTGO watch.

##Bluetooth communication
At this stage, RPi is responsible for synchronization with the TTGO Watch, as the watch reads the bluetooth serial and awaits for certain chars for example 'c', which then leads the watch to go over a synchronization loop.
The session data is in form of: user;weight;steps;distance(m);duration(min);watchID;calories;stoppingTime;\n. Even though calories are calculated in watch, at the end the RPi handles the calories burned calculation, also duration is calculated in RPi.
RPi sends an "r" if the synchronization was successful, otherwise, timeout occurs, session is held in the flash memory and sent other time.
TTGO watch is able to read time, username and bodyweight from bluetooth, which occurs also samelike as stated above. However, the time, user and bodyweight synchronization is not implemented in RPi.




