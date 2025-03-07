
#include <config.hpp>




#define BTN_X_MIN 80
#define BTN_X_MAX 160
#define BTN_Y_MAX 200
#define BTN_Y_MIN 160 
#define SERVICE_UUID "12345678-1234-5678-1234-57777abcdef0"
#define CHARACTERISTIC_UUID "87654321-4321-6789-4321-quebec123456"

TTGOClass *ttgo;
TFT_eSPI *tft;

bool deviceConnected = false;
bool oldDeviceConnected = false;

uint32_t interval = 0;
BLECharacteristic *pCharacteristic;


class MyCallbacks : public BLECharacteristicCallbacks
{
    void onWrite(BLECharacteristic *pCharacteristic)
    {
        return;
        
    }
};


    
class MyServerCallback : public BLEServerCallbacks
{
    void onConnect(BLEServer *pServer)
    {
        deviceConnected = true;
        Serial.println("onConnect");
    }

    void onDisconnect(BLEServer *pServer)
    {
        deviceConnected = false;
        Serial.println("onDisconnect");
    }
};

char buf[128];

void setupBLE(void)
{

    BLEDevice::init("LilyGo-Watch");
    BLEServer *pServer = BLEDevice::createServer();

    pServer->setCallbacks(new MyServerCallback);

    BLEService *pService = pServer->createService(SERVICE_UUID);

    pCharacteristic = pService->createCharacteristic(
            CHARACTERISTIC_UUID,
            BLECharacteristic::PROPERTY_READ |
            BLECharacteristic::PROPERTY_WRITE);

    pCharacteristic->setCallbacks(new MyCallbacks());

    pCharacteristic->setValue("Format: YY,MM,DD,h,m,s");
    pService->start();

    BLEAdvertising *pAdvertising = pServer->getAdvertising();
    pAdvertising->start();
}

bool status;

void drawSTATUS(bool status);



void setup() {
    Serial.begin(115200);
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->openBL();
    tft = ttgo->tft;

    tft->fillScreen(TFT_BLACK);
    tft->setTextFont(2);
    tft->setTextColor(TFT_WHITE, TFT_BLACK);
    tft->drawString("testilaitos", 62, 30);
    tft->fillRect(BTN_X_MIN,BTN_Y_MIN,80,40, TFT_GREEN);
    
    
    
    
   
    
    
   

    setupBLE();
    drawSTATUS(false);

}
void drawSTATUS(bool status)   
{
    
    String str = status ? "Connection" : "Disconnect";
    int16_t cW = tft->textWidth("Connection", 2);
    int16_t dW = tft->textWidth("Disconnect", 2);
    int16_t w = cW > dW ? cW : dW;
    w += 6;
    int16_t x = 160;
    int16_t y = 20;
    int16_t h = tft->fontHeight(2) + 4;
    uint16_t col = status ? TFT_GREEN : TFT_BLUE;
    tft->fillRoundRect(x, y, w, h, 3, col);
    tft->setTextColor(TFT_BLACK, col);
    tft->setTextFont(2);
    tft->drawString(str, x + 2, y);
}
Session CreateSession();
std::vector<uint32_t> result;
std::vector<Session> SessionsSaved;
std::ostringstream oss;
std::string s;
void loop()
{
    if (deviceConnected && oldDeviceConnected) {
        oldDeviceConnected = deviceConnected;
        Serial.println("Draw deviceDisconnected");
        drawSTATUS(false);
    }

    // connecting
    if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
        Serial.println("Draw deviceConnected");
        drawSTATUS(true);
    }
    
    vector<Session> SessionsSaved;
    int16_t x, y;
    ttgo->getTouch(x,y);
    
    if (x >= BTN_X_MIN && x <= BTN_X_MAX && y >= BTN_Y_MIN && y <= BTN_Y_MAX) 
    {
        Session newSession = CreateSession();
    
        tft->fillScreen(TFT_BLACK);
        
        
        result = newSession.getSteps();
        SessionsSaved.push_back(newSession);
        tft->fillRect(BTN_X_MIN,BTN_Y_MIN,80,40, TFT_GREEN);
        pCharacteristic->setValue(newSession.getStringSteps());
    }
    
    

    
    
    
    
}






