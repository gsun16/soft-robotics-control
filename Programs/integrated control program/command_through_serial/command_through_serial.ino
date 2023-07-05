//Pins that connects to corresponding MOSFETs

const int finger[6] = {2, 3, 4, 5, 6, 7}; //finger pins

const int gas_out = 9;  //gas IO
const int pump = 11; //gas pump spd control using pwm

const int pressure = A7; //pressure sensor

//some variables that you can change
int spd = 0; //gas pump speed 255-0, 0 is highest
int p_long = 200; //max pressure for a long finger
int p_short = 200;//max pressure for a short finger

//////////////////////////////////////////////////////////////////
#define numOfValsRec 6
#define digitsPerValRec 1

int valsRec[numOfValsRec];
int valsRec_old[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000

int counter = 0;
bool Start = false;
String recString;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //////////////////////////////////////////
  pinMode(gas_out, OUTPUT);
  for (int i = 0; i < 6; i++) pinMode(finger[i], OUTPUT);
  pinMode(pressure, INPUT);
  Serial.println("initialized");
}


void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '$') {
      Start = true;
    }
    if (Start) {
      if (counter < stringLength) {
        recString = String(recString + c);
        counter ++;
      }
      if (counter >= stringLength) {
        for (int i = 0; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = recString.substring(num, num + digitsPerValRec).toInt();
        }
        recString = "";
        counter = 0;
        Start = false;
      }
    }
  }
}

int change = 0;

void loop() {
  // put your main code here, to run repeatedly:

  for (int j = 0; j < numOfValsRec; j++) {
    if (valsRec_old[j] != valsRec[j]) {
      valsRec_old[j] = valsRec[j];
      change++;
    }
  }
  receiveData();
  if (change != 0) {
    for (int i = 0; i < numOfValsRec; i++) {
      if (valsRec[i] == 1) {
        Bend(i);
      } else {
        Rest(i);
      }
    }
    change = 0;
  }


}

//functions to control actuators or do some gestures

void Bend(int Index) {
  analogWrite(pump, spd);
  digitalWrite(finger[Index], HIGH);
  delay(30);
  if (Index == 0) {
    while (analogRead(pressure) <= p_short) {
      digitalWrite(gas_out, LOW);

      char content[50];
      sprintf(content, "%d th finger, increasing pressure: %d", Index, analogRead(pressure) );
      Serial.println(content);

    }
  }
  else if (Index <= 4 && Index > 0) {
    while (analogRead(pressure) <= p_long) {
      digitalWrite(gas_out, LOW);

      char content[50];
      sprintf(content, "%d th finger, increasing pressure: %d", Index, analogRead(pressure) );
      Serial.println(content);
    }
  }
  else if (Index == 5) {
    while (analogRead(pressure) <= 530) {
      digitalWrite(gas_out, LOW);

      char content[50];
      sprintf(content, "thumb, increasing pressure: %d", analogRead(pressure) );
      Serial.println(content);
    }
  }
  else Serial.println ("error in index");

  char content[50];
  sprintf(content, "Finger %d is bent.", (Index));
  Serial.println(content);
  digitalWrite(finger[Index], LOW);
  analogWrite(pump, 230);
  delay(1000);
}

void Rest(int Index) {
  digitalWrite(finger[Index], HIGH);
  delay(30);
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
