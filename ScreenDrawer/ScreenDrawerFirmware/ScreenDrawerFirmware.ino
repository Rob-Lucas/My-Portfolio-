#include<Wire.h>

const int MPU_addr=0x68;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

void setup(){
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B); 
  Wire.write(0);    
  Wire.endTransmission(true);
  Serial.begin(115200);
}

void loop(){
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true); 
  AcX=Wire.read()<<8|Wire.read();  
  AcY=Wire.read()<<8|Wire.read();  
  AcZ=Wire.read()<<8|Wire.read();  
  Tmp=Wire.read()<<8|Wire.read();  
  GyX=Wire.read()<<8|Wire.read();  
  GyY=Wire.read()<<8|Wire.read();  
  GyZ=Wire.read()<<8|Wire.read();  

  // Remap accelerometer readings
  // map(value, fromLow, fromHigh, toLow, toHigh)
  AcX = map(AcX, -32768, 32767, -60, 60); // Level at -30 goes to 0
  AcY = map(AcY, -32768, 32767, -35, 35); // Level at -5 goes to 0

  // Normalize to -1 to 1
  float x = AcX / 60.0;
  float y = AcY / 35.0;

  Serial.print(x);
  Serial.print(",");
  Serial.println(y);
  
  delay(100);
}

