// A digital frequency selective filter - Integrated with LED Status
// Based on code by A. Kruger, R. Mudumbai, and N. Najeeb

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

// --- PIN DEFINITIONS ---
int analogPin = A1; // Change to A1 as per your hardware setup
int LED = 12;       // Indicator LED on Digital Pin 12

// --- FILTER SETTINGS ---
const int n = 7;    // Filter order
int m = 10;         // Hysteresis averaging window

float den[] = {1.0000, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00};
float num[] = {0.0058, 0.00, -0.015, 0.00, 0.015, 0.00, -0.0058};

float x[n], y[n], yn, s[10];
float threshold_val = 0.02;  

int Ts = 333; // Sample period (microseconds) for 3000Hz

void setup() {
   Serial.begin(1200);
   
   // Speed up ADC conversions
   sbi(ADCSRA, ADPS2);
   cbi(ADCSRA, ADPS1);
   cbi(ADCSRA, ADPS0);

   pinMode(LED, OUTPUT);

   // Initialize buffers to zero
   for (int i = 0; i < n; i++) x[i] = y[i] = 0;
   for (int i = 0; i < m; i++) s[i] = 0;      
   yn = 0;
}

void loop() {
   static unsigned long changet = micros();
   unsigned long t1;
   int val;

   while (1) {
      t1 = micros();

      // Shift past samples
      for (int i = n - 1; i > 0; i--) {
         x[i] = x[i - 1];
         y[i] = y[i - 1];
      }
      for (int i = m - 1; i > 0; i--) s[i] = s[i - 1];

      // Read and scale input
      val = analogRead(analogPin);
      x[0] = val * (5.0 / 1023.0) - 2.5;

      // Difference Equation (The Filter)
      yn = num[0] * x[0];
      for (int i = 1; i < n; i++) {
         yn = yn - den[i] * y[i] + num[i] * x[i];
      }
      y[0] = yn;

      s[0] = abs(2 * yn); // Rectify signal for thresholding

      // Hysteresis: Find peak in current window
      float maxs = 0;
      for (int i = 0; i < m; i++) {
         if (s[i] > maxs) maxs = s[i];
      }

      // Update LED and Serial every 1 second
      if ((micros() - changet) > 1000000) {
         Serial.println(maxs);
         changet = micros(); //  
         
         if (maxs <= threshold_val) {
             digitalWrite(LED, HIGH); // Beam BLOCKED
             Serial.println("ALERT");  // Python will look for this keyword
          } else {
             digitalWrite(LED, LOW);  // Beam RECEIVED
             Serial.println("CLEAR");
          }
      }

      // Timing check to ensure real-time processing
      if ((micros() - t1) > Ts) {
//         Serial.println("MISSED A SAMPLE");
      }
      while ((micros() - t1) < Ts);
   }
}
