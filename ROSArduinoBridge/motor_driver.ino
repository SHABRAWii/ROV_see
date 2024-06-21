#ifdef USE_BASE
   
#ifdef L298_MOTOR_DRIVER
  void initMotorController() {
    digitalWrite(RIGHT_MOTOR_ENABLE, HIGH);
    digitalWrite(LEFT_MOTOR_ENABLE, HIGH);
  }
  
  void setMotorSpeed(int i, int spd) {
    unsigned char reverse = 0;
  
    if (spd < 0)
    {
      spd = -spd;
      reverse = 1;
    }
    if (spd > 255)
      spd = 255;
    
    if (i == LEFT) { 
      if(!spd){
        analogWrite(LEFT_MOTOR_BACKWARD, 255);
        analogWrite(LEFT_MOTOR_FORWARD, 255);
      }
      else if      (reverse == 0) { analogWrite(LEFT_MOTOR_FORWARD, 0); analogWrite(LEFT_MOTOR_BACKWARD, 255); }
      else if (reverse == 1) { analogWrite(LEFT_MOTOR_BACKWARD, 0); analogWrite(LEFT_MOTOR_FORWARD, 255); }
    }
    else /*if (i == RIGHT) //no need for condition*/ {
      if(!spd){
        analogWrite(RIGHT_MOTOR_BACKWARD, 255);
        analogWrite(RIGHT_MOTOR_FORWARD, 255);
      }
      else if      (reverse == 0) { analogWrite(RIGHT_MOTOR_FORWARD, 0); analogWrite(RIGHT_MOTOR_BACKWARD, 255); }
      else if (reverse == 1) { analogWrite(RIGHT_MOTOR_BACKWARD, 0); analogWrite(RIGHT_MOTOR_FORWARD, 255); }
    }
  }
  
  void setMotorSpeeds(int leftSpeed, int rightSpeed) {
    setMotorSpeed(LEFT, leftSpeed);
    setMotorSpeed(RIGHT, rightSpeed);
  }
#else
  #error A motor driver must be selected!
#endif

#endif
