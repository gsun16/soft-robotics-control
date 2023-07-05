//Pins that connects to corresponding MOSFETs

const int finger[5] = {2, 3, 4, 5, 6}; //finger pins
const int palm = 7;
const int gas_out = 9;  //gas IO
const int pump = 11; //gas pump spd control using pwm

const int pressure = A7; //pressure sensor

//some variables that you can change
int spd = 0; //gas pump speed 255-0, 0 is highest
int p_long = 195; //max pressure for a long finger
int p_short = 170;//max pressure for a short finger


void setup() {
  Serial.begin(9600);
  //define pin IO
  pinMode(gas_out, OUTPUT);
  for (int i = 0; i < 5; i++) pinMode(finger[i], OUTPUT);
  pinMode(pressure, INPUT);
  Serial.println("initialized");
}


void loop() {
  rock_sign();
}





//functions to control actuators or do some gestures

void Bend(int Index) {
  analogWrite(pump, spd);
  digitalWrite(finger[Index], HIGH);
  delay(100);
  if (Index == 0) {
    while (analogRead(pressure) <= p_short) {
      digitalWrite(gas_out, LOW);

      char content[50];
      sprintf(content, "%d th finger, increasing pressure: %d", Index, analogRead(pressure) );
      Serial.println(content);

    }
  }
  else if (Index <= 4 || Index > 0) {
    while (analogRead(pressure) <= p_long) {
      digitalWrite(gas_out, LOW);

      char content[50];
      sprintf(content, "%d th finger, increasing pressure: %d", Index, analogRead(pressure) );
      Serial.println(content);
    }
  }
  else Serial.println ("error in index");

  char content[50];
  sprintf(content, "Finger %d is bent.", (Index));
  Serial.println(content);
  digitalWrite(finger[Index], LOW);
  analogWrite(pump, 230);
  delay(500);
}

void Rest(int Index) {
  digitalWrite(finger[Index], HIGH);
  delay(100);
  while (analogRead(pressure) >= 105) {
    digitalWrite(gas_out, HIGH);

    Serial.print(Index);
    Serial.print("th finger, releasing pressure:");
    Serial.println(analogRead(pressure));
  }
  digitalWrite(finger[Index], LOW);
  char content[50];
  sprintf(content, "Finger %d is at rest.", (Index));
  Serial.println(content);
}


void Rest_All() {
  for (int i = 1; i < 5; i++) {
    digitalWrite(finger[i], HIGH);
  }
  delay(100);
  while (analogRead(pressure) >= 105) {
    digitalWrite(gas_out, HIGH);

    Serial.print("all actuators releasing pressure:");
    Serial.println(analogRead(pressure));
  }
  for (int i = 1; i < 5; i++) {
    digitalWrite(finger[i], LOW);
  }

  Serial.println("all fingers are at rest");
}


void move_fingers() {
  for (int i = 0; i < 5; i++) {
    Bend(i);
    delay(1000);
    Rest(i);
    delay(1000);
  }
}
void rock_sign () {
  for (int i = 1; i < 5; i++) {
    Bend(i);
  }
  delay(2000);
  Rest_All();
  delay(1000);
}
