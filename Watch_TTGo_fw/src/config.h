#ifndef SESSION_H
#define SESSION_H

#include <Arduino.h>
#include <LilyGoWatch.h>

#include "BluetoothSerial.h"
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <rtc.h>
#include <string.h>
#include "utils.h"
using namespace std;





extern TFT_eSPI *tft;
extern TTGOClass *ttgo;
extern PCF8563_Class *rtc;

class Session {
    private:
        float disMultiplier = 0.6f; // to convert steps into 
        uint32_t steps; //steps taken during hike
        String name; //user name
        string startingTime; //the day and time when session started
        string stoppingTime;
        float distance; // distance in meters
        float duration; // session duration in minutes
        float startTime; //start timestamp in minutes
        float stopTime;
        double mass = 0.0; // in kgs
        double calories = 0.0; //
    public: 
        
        void setSteps(uint32_t newSteps) {
            steps = newSteps; 
            
        }
        
        uint32_t getSteps() {
            return steps;
        }
        
        string getstartingTime() {
            return startingTime;;
        }
        String getUser() {
            return name;
        }

        void setStartingtime(string newId){
            startingTime = newId;
        }
        void setStoppingtime(string newStoppingtime){
            stoppingTime = newStoppingtime;
        }
        string getstoppingTime() {
            return stoppingTime;
        }
        void setUser(String userName) {
            name = userName;
        }
        float getDistance() {
            return distance;
        }
        void setDistance() {
            distance = steps * disMultiplier;
        }
        void setStartTime(int hour,int minute, int sec){
            
            startTime = hour * 60.000 + minute + sec / 60.000;
            

        }
        void setStopTime(int hour,int minute, int sec){
            
            stopTime = hour * 60.000 + minute + sec / 60.0000;
            

        }
        void setDuration() {
            duration = stopTime - startTime;
        }
        int getDuration() {
            return duration;
        }
        
        string getDurationStr() {
            string result = to_string(duration);
            return result;
        }
        void setMass(double newMass) {
            mass = newMass;
        }
        string getMass(){
            string result = to_string(mass);
            return result;
        }
        string getCalories() {
            string result = to_string(calories);
            return result;
        }
        void setCalories() {
            calories = (duration * mass * 6.0 * 3.5) / 200.0;
        }
    };

    


#endif 

