#include <LilyGoWatch.h>
#include <session.h>
TTGOClass *ttgo;
#define BTN_X_MIN 80
#define BTN_X_MAX 160
#define BTN_Y_MAX 200
#define BTN_Y_MIN 160

char buf[128];

void setup() {
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->openBL();
    ttgo->tft->fillScreen(TFT_BLACK);
    ttgo->tft->setTextFont(2);
    ttgo->tft->setTextColor(TFT_WHITE, TFT_BLACK);
    ttgo->tft->drawString("testilaitos", 62, 30);
    ttgo->tft->fillRect(BTN_X_MIN,BTN_Y_MIN,80,40,TFT_RED);

}

void loop()
{
    int16_t x, y;
    ttgo->getTouch(x,y);
    if (x >= BTN_X_MIN && x <= BTN_X_MAX && y >= BTN_Y_MIN && y <= BTN_Y_MAX) 
    {
      
        
        ttgo->tft->fillScreen(TFT_BLACK);
        int p = createSession();
        ttgo->tft->drawString("testinappulalle", 62, 30);
    }
    
    
}