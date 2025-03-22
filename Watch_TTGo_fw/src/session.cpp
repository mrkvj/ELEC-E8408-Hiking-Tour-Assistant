#include <config.hpp>
bool irq = false;
bool sessionOn = true;



BMA* sensor;
#include <time.h>
#define BTN_X_MIN 80
#define BTN_X_MAX 160
#define BTN_Y_MAX 200
#define BTN_Y_MIN 160







char days[128];
char stopTime[128];
Session CreateSession() {
    ttgo = TTGOClass::getWatch();
    tft = ttgo->tft;
    Session ThisSession;
    rtc = ttgo->rtc;
    sensor = ttgo->bma;
    
    
    
    tft->fillScreen(TFT_BLACK);
    
    RTC_Date t = rtc->getDateTime();
    ThisSession.setStartTime(t.hour,t.minute,t.second);
    
    snprintf(days, sizeof(days), "%s", rtc->formatDateTime(5));
    
    ThisSession.setStartingtime(days);
    
    
    tft->setCursor(45, 90);
    
    // Accel parameter structure
    Acfg cfg;
    /*!
        Output data rate in Hz, Optional parameters:
            - BMA4_OUTPUT_DATA_RATE_0_78HZ
            - BMA4_OUTPUT_DATA_RATE_1_56HZ
            - BMA4_OUTPUT_DATA_RATE_3_12HZ
            - BMA4_OUTPUT_DATA_RATE_6_25HZ
            - BMA4_OUTPUT_DATA_RATE_12_5HZ
            - BMA4_OUTPUT_DATA_RATE_25HZ
            - BMA4_OUTPUT_DATA_RATE_50HZ
            - BMA4_OUTPUT_DATA_RATE_100HZ
            - BMA4_OUTPUT_DATA_RATE_200HZ
            - BMA4_OUTPUT_DATA_RATE_400HZ
            - BMA4_OUTPUT_DATA_RATE_800HZ
            - BMA4_OUTPUT_DATA_RATE_1600HZ
    */
    cfg.odr = BMA4_OUTPUT_DATA_RATE_100HZ;
    /*
        G-range, Optional parameters:
            - BMA4_ACCEL_RANGE_2G
            - BMA4_ACCEL_RANGE_4G
            - BMA4_ACCEL_RANGE_8G
            - BMA4_ACCEL_RANGE_16G
    */
    cfg.range = BMA4_ACCEL_RANGE_2G;
    /*!
        Bandwidth parameter, determines filter configuration, Optional parameters:
            - BMA4_ACCEL_OSR4_AVG1
            - BMA4_ACCEL_OSR2_AVG2
            - BMA4_ACCEL_NORMAL_AVG4
            - BMA4_ACCEL_CIC_AVG8
            - BMA4_ACCEL_RES_AVG16
            - BMA4_ACCEL_RES_AVG32
            - BMA4_ACCEL_RES_AVG64
            - BMA4_ACCEL_RES_AVG128
    */
    cfg.bandwidth = BMA4_ACCEL_NORMAL_AVG4;

    /*! Filter performance mode , Optional parameters:
        - BMA4_CIC_AVG_MODE
        - BMA4_CONTINUOUS_MODE
    */
    cfg.perf_mode = BMA4_CONTINUOUS_MODE;

    // Configure the BMA423 accelerometer
    sensor->accelConfig(cfg);

    // Enable BMA423 accelerometer
    // Warning : Need to use steps, you must first enable the accelerometer
    // Warning : Need to use steps, you must first enable the accelerometer
    // Warning : Need to use steps, you must first enable the accelerometer
    sensor->enableAccel();

    pinMode(BMA423_INT1, INPUT);
    
    attachInterrupt(BMA423_INT1, [] {
        
        irq = 1;
    }, RISING); 

   
    sensor->enableFeature(BMA423_STEP_CNTR, true);
    sensor->resetStepCounter();
    sensor->enableStepCountInterrupt();
    tft->setTextColor(random(0xFFFF));
     
    tft->setTextFont(4);
    tft->setTextColor(TFT_WHITE, TFT_BLACK);

   

    
    
    
    int16_t x, y;
    tft->drawString("Press red button to stop session", 20,20,2);
    tft->fillRect(BTN_X_MIN,BTN_Y_MIN,80,40, TFT_RED);
    while (sessionOn = true) {

        ttgo->getTouch(x,y);    
            if (x >= BTN_X_MIN && x <= BTN_X_MAX && y >= BTN_Y_MIN && y <= BTN_Y_MAX) {
                    sessionOn = false;
                    RTC_Date y = rtc->getDateTime();
                    ThisSession.setStopTime(y.hour,y.minute,y.second);
                    snprintf(stopTime, sizeof(stopTime), "%s", rtc->formatDateTime(5));
    
                    ThisSession.setStoppingtime(stopTime);

                    ThisSession.setDuration();
                        
                    
    
                    
                    
                    
                    
                    return ThisSession;
            }    
            
        if (irq) {
            irq = 0;
            bool  rlst;
            do {
                // Read the BMA423 interrupt status,
                // need to wait for it to return to true before continuing
                rlst = sensor->readInterrupt();
            } 
            
            
            while (!rlst);
            tft->setTextFont(2);
            tft->setCursor(45,80);
            tft->setTextColor(TFT_WHITE, TFT_BLACK);
            tft->print("Distance (m): ");
            
            tft->print(ThisSession.getDistance());
            // Check if it is a step interrupt
            if (sensor->isStepCounter()) {
                // Get step data from register
                uint32_t step = sensor->getCounter();
                
                tft->setCursor(45, 118);
                tft->print("StepCount: ");
                
                
                ThisSession.setSteps(step);
                ThisSession.setDistance();
                tft->print(ThisSession.getSteps());
                
                
                
        
            
                
            }

            
        delay(5);    

            
        }
        

    }
