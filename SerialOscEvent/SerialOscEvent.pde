import java.awt.AWTException;
import java.awt.Robot;
import java.awt.event.KeyEvent;
import java.util.Map;

import processing.serial.*;

import oscP5.*;
import netP5.*;
  
OscP5 oscP5;

KeystrokeSimulator keySim;
Robot robot;

int countLock = 0;
boolean LOOP_IS_ACTIVE = true;
boolean renderTimer = false;

Serial myPort;    // The serial port
int videoID=0;  // Input string from serial port
int startTime;
int lastID = 25;

Map videoDelay = new HashMap();
int actualDelay = 0;

boolean ENABLE_SERIAL = false;

int getSerialDevice()
{
  String[] devices = Serial.list();
  for(int i=0; i < devices.length ;++i)
  {
    println(devices[i]);
    if( devices[i].contains("cu.usbmodem1421") || devices[i].contains("COM3"))
    {
      println("Enable device: "+i);
      return i;
    }
  }
  println(".:FAILED TO INIT SERIAL:.");
  return 0;
}
 
void setup() { 
  size(640,480);

  keySim = new KeystrokeSimulator();
  if( ENABLE_SERIAL )
  {
    myPort = new Serial(this, Serial.list()[getSerialDevice()], 9600); 
    myPort.buffer(2);
  }else
  {
    oscP5 = new OscP5(this,15000);
  }
  
  
  videoDelay.put(KeyEvent.VK_Q,    59000);//81
  videoDelay.put(KeyEvent.VK_W,    53000);//87
  videoDelay.put(KeyEvent.VK_E,    60000);//69
  videoDelay.put(KeyEvent.VK_R,    67000);//82
  videoDelay.put(KeyEvent.VK_T,    67000);//84
  videoDelay.put(KeyEvent.VK_Y,    80000);//89
  videoDelay.put(KeyEvent.VK_U,    87000);//85
  videoDelay.put(KeyEvent.VK_I,    59000);//73
  videoDelay.put(KeyEvent.VK_A,    86000);//65
  videoDelay.put(KeyEvent.VK_S,    52000);//83
  videoDelay.put(KeyEvent.VK_D,    43000);//68
  videoDelay.put(KeyEvent.VK_F,    51000);
  videoDelay.put(KeyEvent.VK_G,    60600);
  videoDelay.put(KeyEvent.VK_H,    48000);
  videoDelay.put(KeyEvent.VK_J,    51000);
  videoDelay.put(KeyEvent.VK_K,    48000);
  videoDelay.put(KeyEvent.VK_Z,    60000);
  videoDelay.put(KeyEvent.VK_X,    51000);
  videoDelay.put(KeyEvent.VK_C,    60000);
  videoDelay.put(KeyEvent.VK_V,    10000);
  videoDelay.put(KeyEvent.VK_B,    10000);
  videoDelay.put(KeyEvent.VK_N,    10000);
  videoDelay.put(KeyEvent.VK_M,    10000);
  videoDelay.put(KeyEvent.VK_COMMA,10000);
  
  fill(0, 102, 153);
  textSize(50);
} 
 
void draw() { 
  background(0); 
  
  if(renderTimer)
  {
    text("Play video: " + Character.toString((char) videoID), 10,50);
    text((int)((millis()-startTime)/1e3),213,240);
  }else
  {
    text("LOOP", 10,50);
  }
  
} 
 
void serialEvent(Serial p) {
  videoID = Integer.parseInt(p.readString());
  
  if(videoDelay.containsKey(videoID))
    actualDelay = (int)videoDelay.get(videoID);
  
  if( videoID != 25 && videoID != lastID)//tag is valid
  {
    lastID = videoID;
    thread("lockFunction");
    try{
    
      keySim.simulate(videoID);
    
    }catch(AWTException e){
      println(e);
    }
  }
}

void lockFunction()
{
  int id = countLock;
  println(".:LOCK "+id+":.");
  renderTimer = true;
  if( LOOP_IS_ACTIVE )
  {
    println("Disable Loop");
    LOOP_IS_ACTIVE = false;
    try{
    
      keySim.simulate(KeyEvent.VK_P);
    
    }catch(AWTException e){
      println(e);
    }
  }
  ++countLock;
  startTime = millis();
  delay(actualDelay);
  println(".:UNLOCK "+id+" "+countLock+":.");
  
  if( (countLock - 1) == id )
  {
    println("Enable Loop");
    LOOP_IS_ACTIVE = true;
    renderTimer = false;
    lastID = 0;
    try{
    
      keySim.simulate(KeyEvent.VK_P);
    
    }catch(AWTException e){
      println(e);
    }
  }
}

/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage theOscMessage) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.");
  print(" addrpattern: "+theOscMessage.addrPattern());
  println(" typetag: "+theOscMessage.typetag());
  println(" arguments: "+theOscMessage.arguments()[0].toString());
  
  videoID = Integer.parseInt(theOscMessage.arguments()[0].toString());
  
  if(videoDelay.containsKey(videoID))
    actualDelay = (int)videoDelay.get(videoID);
  
  if( videoID != 25 && videoID != lastID)//tag is valid
  {
    lastID = videoID;
    //thread("lockFunction");
    try{
    
      keySim.simulate(videoID);
      if(videoID != KeyEvent.VK_D
      && videoID != KeyEvent.VK_P)
      {
        keySim.simulate(KeyEvent.VK_P);
      }
    
    }catch(AWTException e){
      println(e);
    }
  }
}