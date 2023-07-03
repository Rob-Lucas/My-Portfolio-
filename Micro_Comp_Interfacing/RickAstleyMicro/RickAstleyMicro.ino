#include <Keyboard.h>

unsigned long interval = 220000; // Interval of 3 minutes and 40 seconds in milliseconds
unsigned long previousMillis = 0;

void setup() {
  Keyboard.begin();
  delay(2000); // Delay for 2 seconds to allow system recognition
  openRickRollURL();
  Serial.begin(9600);
  Serial.print("Rick Astley sends his regards! He will never desert you!");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) { // <------- This part runs the song every 3:40 min which is when the song ends.
    previousMillis = currentMillis; // Reset the timer
    
    openRickRollURL(); // Run the RickRoll code
  }

  // Other code or tasks can be added here
}

void openRickRollURL() {
  Keyboard.press(KEY_LEFT_GUI); // Press the Windows key or Command key (for macOS)
  Keyboard.press('r'); // Open the Run dialog
  Keyboard.releaseAll();
  delay(1000);
  
  Keyboard.print("https://www.youtube.com/watch?v=dQw4w9WgXcQ"); // Enter the Rick Astley video URL
  Keyboard.press(KEY_RETURN); // Press Enter to open the URL
  Keyboard.releaseAll();

  delay(1000); // Delay to allow the YouTube page to load

  // Press the spacebar key to potentially start the video
  Keyboard.press(' ');
  Keyboard.release(' ');
}
