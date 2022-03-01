#include <Servo.h>

Servo upper;
Servo lower;

//global vars
int serial_input = 0;
int up_position = 90;
int low_position = 90;
char last = "";
bool nd = False;
bool nd_vals = False;
int del = 15;

void setup() {
  upper.attach(10);
  lower.attach(9);
  Serial.begin(9600);
  upper.write(up_position);
  lower.write(low_position);
}

void upd_servos(){
  upper.write(up_position);
  lower.write(low_position);  
}

void upper_control(int in){
  up_position += in;
  upper.write(up_position);
}

void lower_control(int in){
  low_position += in;
  lower.write(low_position);  
}

void loop() {
  if (Serial.available() > 0){
    serial_input = Serial.read();
    Serial.print(char(serial_input));
    Serial.println("");

    switch(char(serial_input)){
      case 'L':
        lower_control(-1);
        nd = False;
        break;
      case 'R':
        lower_control(1);
        nd = False;
        break;
      case 'U':
        upper_control(1);
        nd = False;
        break;
      case 'D':
        upper_control(-1);
        nd = False;
        break;
      case 'N':
        nd = True;
        break; 
    }
    
    if(last==char(serial_input)){
      switch(char(serial_input)){
        case 'L':
          lower_control(-1);
          nd = False;
          break;
        case 'R':
          lower_control(1);
          nd = False;
          break;
        case 'U':
          upper_control(1);
          nd = False;
          break;
        case 'D':
          upper_control(-1);
          nd = False;
          break;
        case 'N':
          nd = True;
          break;          
      }
    }
    last=char(serial_input);
    del = 15;
  }
  else{
    if(nd){
      if(up_position >=180 || low_position >=180){
        nd_vals = True;
        up_position = 180;
        low_position = 180;
      }
      else if(up_position <=0 || low_position <= 0){
        nd_vals = False
        up_position = 0;
        low_position = 0;
      }

      if(nd_vals){
        up_position--;
        low_position--;
      }
      else{
        up_position++;
        low_position++;
      }
      upd_servos();
      del = 250;     
    }    
  }  
  delay(del);
}
