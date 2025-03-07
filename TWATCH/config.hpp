
#ifndef SESSION_H
#define SESSION_H

#include <BLEDevice.h>
#include <BLEClient.h>
#include <BLEServer.h>
#include <BLEUtils.h>



#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <LilyGoWatch.h>
#include <rtc.h>
#include <string.h>
using namespace std;
#include <LilyGoWatch.h>

extern TFT_eSPI *tft;
extern TTGOClass *ttgo;
extern PCF8563_Class *rtc;

class Session {
    private:
        std::vector<uint32_t> steps = {0};
        int calories;
        std::string name;
        std::string id;
        
    public:
        std::vector<uint32_t> getSteps() {
            return steps;
        }
           
        double getCalories() {
            return calories;
        }
        void setCalories(int newCalories) {
            calories = newCalories;

        }
        
        void setSteps(uint32_t newSteps) {
            steps.push_back(newSteps); 
            
        }
        uint32_t getLastStep() {
            return steps.back();
        }
        string getStringSteps() {
            std::ostringstream oss;
            for (uint32_t num : steps) {
                
                oss << num << " ";  // Convert numbers to space-separated string
            }
            std::string s = oss.str(); 
            return s;  
        }
        
    };

    


#endif 

