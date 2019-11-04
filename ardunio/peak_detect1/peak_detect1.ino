int left_sensorPin = A0;        // Pin to read from
int right_sensorPin = A1; 

//int left_previousSample = 0;   // Value of the sensor the last time around
//int right_previousSample = 0;
//
//int threshold = 500;      // Threshold sample value
//
//// For method 2 only
//int previousState = 0;
//int hysteresis = 50;

// For method 3 only
int left_peakValue = 0;
int right_peakValue = 0;

int thresholdToTrigger = 500;
int amountBelowPeak = 100;
int rolloffRate = 1;

int left_triggered = 0;
int right_triggered = 0;
int left_bang = 0;
int right_bang = 0;

void setup() {
  Serial.begin(9600);  // Turn on the serial port
}

void loop() {
  int left_currentSample = analogRead(left_sensorPin);
  int right_currentSample = analogRead(right_sensorPin);
//  Serial.println("left: "+String(left_currentSample)+"right: "+String(right_currentSample));

  // METHOD 1: Simple thresholding
//  if(currentSample > threshold && previousSample <= threshold)
//    Serial.println("bang");
//  previousSample = currentSample;


  // METHOD 2: Thresholding with hysteresis
  // Hint: use the hysteresis variable that has already been defined for you.
//  if(previousState == 0) {
//    // Previous state was below the threshold
//    if(currentSample > threshold) {
//      // State crossed the threshold in the positive direction. Send trigger.
//      previousState = 1;
//      Serial.println("bang");
//    }
//  }
//  else {
//    if(currentSample < threshold-hysteresis)
//      previousState = 0;
//  }
  
  // METHOD 3: peak detection. Look for a downward trend in the data
  // when the current value is above a minimum threshold. A decrease from
  // the last sample to this one means the last sample was a peak. We use
  // the threshold to make sure the peak was sufficiently high to not just
  // be noise. The disadvantage here is that the triggering is slower since
  // we have to wait for *after* the peak passes to figure out it happened.
  // But the advantage is that we can measure its exact height.
  
  if(left_currentSample > left_peakValue) { // Record the highest incoming sample
    left_peakValue = left_currentSample;
    left_triggered = 0;
  }
  else if(left_peakValue >= rolloffRate) // But have the peak value decay over time
    left_peakValue -= rolloffRate;       // so we can catch the next peak later
    
  if(right_currentSample > right_peakValue) {
    right_peakValue = right_currentSample;
    right_triggered = 0;
  }
  else if(right_peakValue >= rolloffRate)
    right_peakValue -= rolloffRate;
    
  if(left_triggered==0 && left_peakValue>=thresholdToTrigger && left_currentSample<left_peakValue-amountBelowPeak) {
    left_bang = 1;  // Serial.println(peakValue);
    Serial.println("left_bang");
    left_triggered = 1; // Indicate that we've triggered and wait for the next peak before triggering
                   // again.
  }else{
    left_bang = 0;
    }

  if(right_triggered==0 && right_peakValue>=thresholdToTrigger && right_currentSample<right_peakValue-amountBelowPeak) {
    right_bang = 1; //  Serial.println(peakValue);
    Serial.println("right_bang");
    right_triggered = 1; // Indicate that we've triggered and wait for the next peak before triggering
                   // again.
  }else{
    right_bang = 0;
    }

//  Serial.println("L"+String(left_bang)+"R"+String(right_bang));
  delay(1);
}
