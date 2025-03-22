#include <config.hpp>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
String userID;
string watchID = "TWATCH-TTGO"; //acts as a "Serialnumber"
String userName = "unnamed";
#define BTN_X_MIN 80
#define BTN_X_MAX 160
#define BTN_Y_MAX 200
#define BTN_Y_MIN 160 
#define SERVICE_UUID "12345678-1234-5678-1234-57777abcdef0"
#define CHARACTERISTIC_UUID "87654321-4321-6789-4321-quebec123456"

TTGOClass *ttgo;
TFT_eSPI *tft;
PCF8563_Class *rtc;
uint32_t interval = 0;

unsigned long last, updateTimeout;
float mass;
volatile bool irqBMA = false;
volatile bool irqButton = false;
bool sessionSent = false;
bool sessionStored = false;



bool setDateTimeFormBLE(const char *str)
{
    /*
    Parse data from BL stream
    */
    uint16_t year; 
    uint8_t month,  day, hour,  min,  sec;
    String temp, data;
    int r1, r2;
    if (str == NULL)return false;

    data = str;

    r1 = data.indexOf(',');
    if (r1 < 0)return false;
    temp = data.substring(0, r1);
    year = (uint16_t)temp.toInt();

    r1 += 1;
    r2 = data.indexOf(',', r1);
    if (r2 < 0)return false;
    temp = data.substring(r1, r2);
    month = (uint16_t)temp.toInt();

    r1 = r2 + 1;
    r2 = data.indexOf(',', r1);
    if (r2 < 0)return false;
    temp = data.substring(r1, r2);
    day = (uint16_t)temp.toInt();

    r1 = r2 + 1;
    r2 = data.indexOf(',', r1);
    if (r2 < 0)return false;
    temp = data.substring(r1, r2);
    hour = (uint16_t)temp.toInt();

    r1 = r2 + 1;
    r2 = data.indexOf(',', r1);
    if (r2 < 0)return false;
    temp = data.substring(r1, r2);
    min = (uint16_t)temp.toInt();

    r1 = r2 + 1;
    temp = data.substring(r1);
    sec = (uint16_t)temp.toInt();

    
    Serial.printf("SET:%u/%u/%u %u:%u:%u\n", year, month, day, hour, min, sec);
    rtc->setDateTime(year, month, day, hour, min, sec);

    return true;
}



void setup() {
    Serial.begin(115200);
    SerialBT.begin("TTGO-Watch");
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->openBL();
    tft = ttgo->tft;
    tft->fillScreen(TFT_BLACK);
    tft->setTextFont(2);
    tft->setTextColor(TFT_WHITE, TFT_BLACK);
    tft->drawString("testilaitos", 62, 30);
    
    rtc = ttgo->rtc;

    
    


    //Side button
    pinMode(AXP202_INT, INPUT_PULLUP);
    attachInterrupt(AXP202_INT, [] {
        irqButton = true;
    }, FALLING);

    //!Clear IRQ unprocessed first
    ttgo->power->enableIRQ(AXP202_PEK_SHORTPRESS_IRQ, true);
    ttgo->power->clearIRQ();
    if(!LITTLEFS.begin(FORMAT_LITTLEFS_IF_FAILED)){
        Serial.println("LittleFS Mount Failed");
        return;
     }
     else{
         Serial.println("Little FS Mounted Successfully");
     }
     
}









double readMassFromBL()  //Read the user name from the bluetooth serial stream
{
    const int maxLength = 5;  
    char mass[maxLength + 1] = "";  
    int index = 0;

    
    unsigned long startTime = millis();  // Record the start time
    const unsigned long timeout = 5000; 
    while (millis() - startTime < timeout) 
    {
        while (SerialBT.available())  
        {
            char incomingChar = SerialBT.read();  

            if (incomingChar == ';')  
            {
                mass[index] = '\0'; 
                
                return atof(mass); 
            }

            if (index < maxLength - 1) 
            {
                mass[index++] = incomingChar;
            }
            startTime = millis();
        }

        delay(5);  
    }
    return 0.0;
}
    
void sendDataBT(fs::FS &fs, const char * path)
{
    /* Sends data via SerialBT */
    File file = fs.open(path);
    if(!file || file.isDirectory()){
        Serial.println("- failed to open file for reading");
        return;
    }
    Serial.println("- read from file:");
    while(file.available()){
        SerialBT.write(file.read());
        
    }
    file.close();
}

void sendSessionBT()
{
    // Read session and send it via SerialBT
    tft->fillRect(0, 0, 240, 240, TFT_BLACK);
    tft->drawString("Sending session", 20, 80);
    tft->drawString("to Hub", 80, 110);

    // Sending session id
    sendDataBT(LITTLEFS, "/data.txt");
    return;
    
}

String readTimeFromBL()  //Read the user name from the bluetooth serial stream
{
    const int maxLength = 50;  
    char time[maxLength + 1] = "";  
    int index = 0;

    tft->fillScreen(TFT_BROWN);
    unsigned long startTime = millis();  // Record the start time
    const unsigned long timeout = 5000; 
    while (millis() - startTime < timeout) 
    {
        while (SerialBT.available()) 
        {
            char incomingChar = SerialBT.read();  

            if (incomingChar == ';')  
            {
                time[index] = '\0';  // Null-terminate the string
                return String(time);  // Convert char array to String
            }

            if (index < maxLength - 1)  // Prevent buffer overflow
            {
                time[index++] = incomingChar;
            }
            startTime = millis();
        }

        delay(5);  // Reduced delay for better responsiveness
    }
    return "";
}


String readUserFromBL()  //Read the user name from the bluetooth serial stream
{
    const int maxLength = 50;  
    char userName[maxLength + 1] = "";  
    int index = 0;

    
    unsigned long startTime = millis();  // Record the start time
    const unsigned long timeout = 5000; 
    while (millis() - startTime < timeout) 
    {
        while (SerialBT.available()) 
        {
            char incomingChar = SerialBT.read();  

            if (incomingChar == ';')  
            {
                userName[index] = '\0';  // Null-terminate the string
                return String(userName);  // Convert char array to String
            }

            if (index < maxLength - 1)  // Prevent buffer overflow
            {
                userName[index++] = incomingChar;
            }
            startTime = millis();
        }

        delay(5);  // Reduced delay for better responsiveness
    }
    return "";
}


void saveStepsToFile(uint32_t step_count)
{
    char buffer[10];
    itoa(step_count, buffer, 10);
    appendFile(LITTLEFS, "/data.txt", buffer);
    appendFile(LITTLEFS, "/data.txt", ";");
}

void saveDistanceToFile(float distance)
{
    char buffer[10];
    snprintf(buffer,10,"%.2f" ,distance);
    appendFile(LITTLEFS, "/data.txt", buffer);
    appendFile(LITTLEFS, "/data.txt", ";");
}

void deleteSession()
{
    deleteFile(LITTLEFS, "/data.txt");

    
}

void saveUserToFile(String user, string mass) {
    
    appendFile(LITTLEFS, "/data.txt", user.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
    
    appendFile(LITTLEFS, "/data.txt", mass.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
    
}

void saveIdToFile(string id) {
    appendFile(LITTLEFS, "/data.txt", id.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
}


void saveDurationToFileStr(string duration) {
    appendFile(LITTLEFS, "/data.txt", duration.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
}
void saveWatchIdToFileStr(string watchID) {
    appendFile(LITTLEFS, "/data.txt", watchID.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
}
void saveCaloriesToFile(string calories) {
    
    appendFile(LITTLEFS, "/data.txt", calories.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
    
}
void saveStopSessionStrToFile(string id) {
    appendFile(LITTLEFS, "/data.txt", id.c_str());
    appendFile(LITTLEFS, "/data.txt", ";");
    appendFile(LITTLEFS, "/data.txt", "\n");
}

Session CreateSession();

int state = 1;
void loop()
{
    switch (state)
    {
    case 1:
    {   
        tft->fillScreen(TFT_BLACK);
        tft->setTextFont(2);
        tft->setCursor(10,10);
        tft->print("User: ");
        
        tft->print(userName);
        tft->drawString("Hiking Watch",  45, 60, 4);
        tft->drawString("Press button", 45, 90, 2);
        tft->drawString("to start session", 45,110,2);
        bool exitSync = false;

        //Bluetooth discovery
        while (1)
        {
            /* Bluetooth sync */
            if (SerialBT.available())
            {
                char incomingChar = SerialBT.read();
                if (incomingChar == 'c' and sessionStored and not sessionSent)
                {
                    sendSessionBT();
                    sessionSent = true;
                }
                if (incomingChar =='t'){
                    userName = readUserFromBL();
                    state = 1;
                    break;
                }
                if (incomingChar == 'm') {
                    mass = readMassFromBL();
                    state = 1;
                    break;
                }
                if (incomingChar =='y') {
                    String time = readTimeFromBL();
                    bool timeSet = setDateTimeFormBLE(time.c_str());
                    state = 1;
                    break;
                }
                if (incomingChar =='u') {
                    userID = readUserFromBL();
                    
                    state = 1;
                    break;
                }
                
                if (sessionSent && sessionStored) {
                    // Update timeout before blocking while
                    updateTimeout = millis();
                    
                    while(1)
                    {
                        

                        if (SerialBT.available())
                            incomingChar = SerialBT.read();
                            
                        if (incomingChar == 'r')
                        {
                            Serial.println("Got an R");
                            // Delete session
                            deleteSession();
                            sessionStored = false;
                            sessionSent = false;
                            incomingChar = 'q';
                            exitSync = true;
                            break;
                        }
                        if ((millis() - updateTimeout > 1000))
                        {
                            Serial.println("Waiting for timeout to expire");
                            
                            sessionSent = false;
                            exitSync = true;
                            break;
                        }
                    }
                }
            }
            if (exitSync)
            {
                state = 1;
                exitSync = false;
                break;

            }

            /*      IRQ     */
            if (irqButton) {
                irqButton = false;
                ttgo->power->readIRQ();
                if (state == 1)
                {
                    state = 2;
                }
                ttgo->power->clearIRQ();
            }
            if (state == 2) {
                if (sessionStored)
                {
                    
                    state = 2;
                }
                break;
            }
        }
        break;
    }
    
    case 2:
    {
        /* Hiking session initalisation */
        
        state = 3;
        break;
    }
    case 3:
    {
        
        /* Hiking session ongoing */
        Session newSession = CreateSession();
        
        newSession.setUser(userName);
        newSession.setMass(mass);
        newSession.setCalories();
        saveUserToFile(newSession.getUser(),newSession.getMass());
        saveIdToFile(newSession.getstartingTime()); 
        saveStepsToFile(newSession.getSteps()); 
        saveDistanceToFile(newSession.getDistance()); // meters
        saveDurationToFileStr(newSession.getDurationStr()); //minutes
        saveWatchIdToFileStr(watchID);
        saveCaloriesToFile(newSession.getCalories());
        saveStopSessionStrToFile(newSession.getstoppingTime());
        sessionStored = true;
        // last to be printed has to be formatted data;\n
        //user;weight;steps;distance(m);duration(min);watchID;calories;stoppingTime;\n
       
            
    }   
      
        
        

        
    
    case 4:
    {
        //Save hiking session data
        delay(1000);
        state = 1;  
        break;
    }
    default:
        // Restart watch
        ESP.restart();
        break;
    }   

}
