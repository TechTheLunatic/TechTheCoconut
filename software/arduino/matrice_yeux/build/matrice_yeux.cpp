//We always have to include the library
#include "LedControl.h"

/*
 By Fabien BERNARD
 
 Configuration : 
 pin 12 is connected to the DataIn 
 pin 11 is connected to the CLK 
 pin 10 is connected to LOAD 
 We have four MAX7219.
 */
#include "WProgram.h"
void setup();
void cylon();
void balayageH();
void balayageV();
void gauchedroite();
void cercle();
void emoticon(int mode);
void writeChar(int eye,char value);
void compteARebours(int time);
void pacman();
void sopalint();
void cardio();
void choukette();
void loop();
LedControl lc=LedControl(12,11,10,4);

/* we always wait a bit between updates of the display */
unsigned long delaytime=30;

void setup() {
  /*
   The MAX72XX is in power-saving mode on startup,
   
   */
   for(int addr=0;addr<=3;addr++)
   {
    // we have to do a wakeup call
    lc.shutdown(addr,false);
    
    // Set the brightness to a maximum value
    lc.setIntensity(addr,15);
    
    // and clear the display
    lc.clearDisplay(addr); 
    
    // and set size off matrix
    lc.setScanLimit(addr, 6);
   }
}

void cylon()
{
  //Aller
  for(int col=0; col<=13 ; col++)
  {
    lc.setEyeColumn(1,col,B11111111,true); //Switch ON
    lc.setEyeColumn(1,col+1,B11111111,true);
    if(col<6)
    delay(delaytime*col/3);
    else
    delay(delaytime*(13-col)/3);
    lc.setEyeColumn(1,col,(byte)0,true); //Switch OFF
    lc.setEyeColumn(1,col+1,(byte)0,true);
  }
  
  //Retour
  for(int col=13; col>=0 ; col--)
  {
    lc.setEyeColumn(1,col,B11111111,true); //Switch ON
    lc.setEyeColumn(1,col-1,B11111111,true);
    if(col<6)
    delay(delaytime*col/3);
    else
    delay(delaytime*(13-col)/3);
    lc.setEyeColumn(1,col,(byte)0,true); //Switch OFF
    lc.setEyeColumn(1,col-1,(byte)0,true);
  }
}
void balayageH()
{
   // Aller
  for(int eye=1 ; eye<=2 ; eye++)
    {
      for (int row=0;row<=6;row++)
      {
        lc.setEyeRow(eye,row,B11111111);
        delay(delaytime);
        lc.setEyeRow(eye,row,(byte)0);
      }
  }
  
   // Retour
  for(int eye=2 ; eye>0 ; eye--)
    {
      for (int row=6;row>=0;row--)
      {
        lc.setEyeRow(eye,row,B11111111);
        delay(delaytime);
        lc.setEyeRow(eye,row,(byte)0);
      }
  }
}

void balayageV()
{
  // Aller
  for(int eye=1 ; eye<=2 ; eye++)
    {
      for (int col=0;col<=13;col++)
      {
        lc.setEyeColumn(eye,col,B11111111,0);
        delay(delaytime);
        lc.setEyeColumn(eye,col,(byte)0,0);
      }
  }
  
   // Retour
  for(int eye=2 ; eye>0 ; eye--)
    {
      for (int col=13;col>=0;col--)
      {
        lc.setEyeColumn(eye,col,B11111111,0);
        delay(delaytime);
        lc.setEyeColumn(eye,col,(byte)0,0);
      }
  }
}

void gauchedroite() // Oeil qui regarde de gauche \u00e0 droite
{
   byte sprite[6]={B00111001,B01111101,B11000111,B11000111,B01111101,B00111001}; 
   byte clignement[6]={B00110001,B00110001,B00110001,B00110001,B00110001,B00110001};
   //byte clignement[7]={B00110001,B00110001,B00110001,B00110001,B00110001,B00110001,B00110001};
  // byte sprite[7]={B00100100,B01010100,B11111110,B01010100,B11111110,B01010100,B01001000}; //Dollars
   
   
   //Centre vers le bord (pour respecter la boucle)
    for (int i=2; i>=0 ; i --)
     {
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, sprite[col], false); 
           lc.setEyeColumn(2, col+i, sprite[col], false); 
        }
        delay(delaytime);
        if(i==3) delay(1000); //Pause
        
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, (byte)0, false); 
           lc.setEyeColumn(2, col+i, (byte)0, false); 
        } 
     }
     
   for(int tour=0; tour<4 ; tour++)
   {    
      //Aller
     for (int i=0; i<8 ; i ++)
     {
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, sprite[col], false); 
           lc.setEyeColumn(2, col+i, sprite[col], false); 
        }
        delay(delaytime);
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, (byte)0, false); 
           lc.setEyeColumn(2, col+i, (byte)0, false); 
        } 
     }
     
     //Retour
     for (int i=8; i>=0 ; i--)
      {
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, sprite[col], false); 
           lc.setEyeColumn(2, col+i, sprite[col], false); 
        }
        delay(delaytime);
        if(i==0 || i==8) delay(delaytime*10);
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, (byte)0, false); 
           lc.setEyeColumn(2, col+i, (byte)0, false); 
        } 
     }
   }
   
   //Arr\u00eat au mileu
   for (int i=0; i<4 ; i ++)
   {
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+i, sprite[col], false); 
         lc.setEyeColumn(2, col+i, sprite[col], false); 
      }
      delay(delaytime);
      if(i==3) delay(1000); //Pause
      
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+i, (byte)0, false); 
         lc.setEyeColumn(2, col+i, (byte)0, false); 
      } 
   }
   
   //Clignement
   for (int tour=0; tour<1; tour ++)
   {
     for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+3, clignement[col], false);  //clin d'oeil
         lc.setEyeColumn(2, col+3, sprite[col], false);
      }
      delay(300);
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+3, (byte)0, false); 
         lc.setEyeColumn(2, col+3, (byte)0, false); 
         lc.setEyeColumn(1, col+3, sprite[col], false); 
         lc.setEyeColumn(2, col+3, sprite[col], false); 
      }
      delay(500);
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+3, (byte)0, false); 
         lc.setEyeColumn(2, col+3, (byte)0, false); 
      }
   } 
}
void cercle() // by cassou
{
   byte sprite1[14]={B11111110,B11111110,B00000000,B11111110,B11111110,B11000110,B11010110,B11010110,B11000110,B11111110,B11111110,B00000000,B11111110,B11111110};
   byte sprite2[14]={B11111110,B00000000,B11111110,B11111110,B10000010,B10111010,B10111010,B10111010,B10111010,B10000010,B11111110,B11111110,B00000000,B11111110};
   byte sprite3[14]={B00000000,B11111110,B11111110,B00000000,B01111100,B01111100,B01101100,B01101100,B01111100,B01111100,B00000000,B11111110,B11111110,B00000000}; 
   
   for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, sprite1[col], true); 
    }
    delay(delaytime*4);
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true); 
       lc.setEyeColumn(1, col, sprite2[col], true); 
    } 
    delay(delaytime*4);
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true); 
       lc.setEyeColumn(1, col, sprite3[col], true); 
    } 
    delay(delaytime*4);
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true); 
    } 
}

void emoticon(int mode)
{
  byte love[14]={B00000000,B00000000,B00000000,B01100000,B11110000,B11111000,B01111100,B00111110,B01111100,B11111000,B11110000,B01100000,B00000000,B00000000}; 
  byte exptdr[14]={B11000110,B11000110,B11000110,B11000110,B11000110,B11101110,B11101110,B11101100,B01101100,B01101100,B01101100,B00111000,B00111000,B00111000};
  byte smiley[14]={B00000111,B00011111,B00111001,B01100001,B11100001,B11000001,B11000001,B11000001,B11000001,B01100001,B01100001,B00111001,B00011111,B00000111};
  byte disturbed[14]={B00011100,B00100010,B01001000,B10010100,B10100010,B10101010,B10101010,B10101010,B10101010,B10101010,B10101010,B10010010,B01000100,B00111000};
  byte doublenote[14]={B00000000,B00000000,B00000100,B00001110,B00001110,B11111110,B11000000,B11000000,B11000100,B11001110,B11001110,B11111110,B00000000,B00000000};
  byte KO[14]={B00000000,B00000000,B00000000,B10000010,B11000110,B01101100,B00111000,B01101100,B11000110,B10000010,B00000000,B00000000,B00000000,B00000000};
  byte blazed1[14]={B11110000,B11110000,B00000000,B00000000,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000000};
  byte blazed2[14]={B00000000,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000110,B00000000,B00000000,B00000000,B00000000};
  byte G[14]={B00000000,B00000000,B00000000,B01111100,B11111100,B11000110,B11000110,B11010110,B11011110,B11011110,B00010000,B00000000,B00000000,B00000000};
  
  for (int col=0; col<13; col++)
   {
     switch(mode)
     {
       case 1: //love
         lc.setEyeColumn(1, col, love[col], true); 
         break;
         
       case 2: //exptdr
         lc.setEyeColumn(1, col, exptdr[col], true); 
         break;
         
       case 3: //smiley
         lc.setEyeColumn(1, col, smiley[col], true); 
         break;
        
        case 4: //disturbed
          lc.setEyeColumn(1, col, disturbed[col], false); 
          lc.setEyeColumn(2, col, disturbed[col], false); 
          break;
          
         case 5: //doublenote
          lc.setEyeColumn(1, col, doublenote[col], false); 
          lc.setEyeColumn(2, col, doublenote[col], false); 
          break;
          
         case 6: //KO
           lc.setEyeColumn(1, col, KO[col], true); 
           break;
          
         case 7: //Blazed
           lc.setEyeColumn(1, col, blazed1[col], false); 
           lc.setEyeColumn(2, col, blazed2[col], false); 
           break;
           
         case 8: // GG
           lc.setEyeColumn(1, col, G[col], false); 
           lc.setEyeColumn(2, col, G[col], false); 
           break;
     }
   }
 
  delay(1000); // pause
  
  //ClearDisplay
  for (int col=0; col<13; col++)
  {
     lc.setEyeColumn(1, col, (byte)0, true);
  }  
}

void writeChar(int eye,char value)
{
  //Sprites
  byte write0[14]={B00000000,B00000000,B00000000,B11111110,B11111110,B11000110,B11000110,B11000110,B11000110,B11111110,B11111110,B00000000,B00000000,B00000000};
  byte write1[14]={B00000000,B00000000,B00000000,B00000000,B00000000,B01000010,B11111110,B11111110,B00000010,B00000000,B00000000,B00000000,B00000000,B00000000};
  byte write2[14]={B00000000,B00000000,B00000000,B00000000,B11011110,B11011110,B11010110,B11010110,B11110110,B11110110,B00000000,B00000000,B00000000,B00000000};
  byte write3[14]={B00000000,B00000000,B00000000,B00000000,B11000110,B11000110,B11010110,B11010110,B11111110,B11111110,B00000000,B00000000,B00000000,B00000000};
  byte write4[14]={B00000000,B00000000,B00000000,B00000000,B00001100,B00011100,B00111100,B01101100,B11001100,B11011110,B11011110,B00000000,B00000000,B00000000};
  byte write5[14]={B00000000,B00000000,B00000000,B00000000,B11110110,B11110110,B11010110,B11010110,B11011110,B11011110,B00000000,B00000000,B00000000,B00000000};
  byte write6[14]={B00000000,B00000000,B00000000,B00000000,B11111110,B11111110,B11011110,B11010010,B11011110,B11011110,B00000000,B00000000,B00000000,B00000000};
  byte write7[14]={B00000000,B00000000,B00000000,B00000000,B11000000,B11001110,B11011110,B11110000,B11100000,B11000000,B00000000,B00000000,B00000000,B00000000};
  byte write8[14]={B00000000,B00000000,B00000000,B00000000,B11111110,B11111110,B11010110,B11010110,B11111110,B11111110,B00000000,B00000000,B00000000,B00000000};
  byte write9[14]={B00000000,B00000000,B00000000,B00000000,B11110110,B11110110,B11010110,B11010110,B11111110,B11111110,B00000000,B00000000,B00000000,B00000000};
  
  for (int col=0; col<13; col++)
  {
     switch(value)
     {
       case 0:
         lc.setEyeColumn(eye, col, write0[col], false);
         break;
       case 1:
         lc.setEyeColumn(eye, col, write1[col], false);
         break;
       case 2:
         lc.setEyeColumn(eye, col, write2[col], false);
         break;
       case 3:
         lc.setEyeColumn(eye, col, write3[col], false);
         break;
       case 4:
         lc.setEyeColumn(eye, col, write4[col], false);
         break;
       case 5:
         lc.setEyeColumn(eye, col, write5[col], false);
         break;
       case 6:
         lc.setEyeColumn(eye, col, write6[col], false);
         break;
       case 7:
         lc.setEyeColumn(eye, col, write7[col], false);
         break;
       case 8:
         lc.setEyeColumn(eye, col, write8[col], false);
         break;
       case 9:
         lc.setEyeColumn(eye, col, write9[col], false);
         break;
     }
  }
}

void compteARebours(int time)
{
  int unite, dizaine;
  for(int i=time;i>=0;i--)
  {
    //Affichage
    unite = i%10;
    dizaine = (i/10)%10;
    
    writeChar(1,dizaine);
    writeChar(2,unite);
    
    //Pause d'une seconde
    delay(1000);
    
    //ClearDisplay
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true);
    }  
  }
}

void pacman()
{
  byte pacman1[8]={B00111000,B01111100,B11111110,B11111110,B11111110,B11101110,B01000100,B00000000};
  byte pacman2[8]={B00111000,B01111100,B11111110,B11111110,B11111110,B11111110,B01111100,B00111000};
  
  for(int i=0;i<28;i++)
  {
    //Pacman
    for(int col=0;col<8;col++)
    {
       if(i%2==0)
       lc.setMatrixColumn(col+i,pacman1[col]);
       else
       lc.setMatrixColumn(col+i,pacman2[col]);
    }
    
    //Points
    if(i+5<10)
    lc.setLed(1,3,3,true);
    if(i+5<15)
    lc.setLed(2,2,3,true);
    if(i+5<20)
    lc.setLed(2,6,3,true);
    if(i+5<25)
    lc.setLed(3,4,3,true);
    
    delay(200);
    //ClearDisplay
    for (int col=0; col<15; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true);
    }
    
    //Points
    if(i+5<10)
    lc.setLed(1,3,3,true);
    if(i+5<15)
    lc.setLed(2,2,3,true);
    if(i+5<20)
    lc.setLed(2,6,3,true);
    if(i+5<25)
    lc.setLed(3,4,3,true);
  }
  
  /*
  //Win !
  
  byte writeW[14]={B11000000,B11110000,B00111100,B00001110,B00001110,B00111100,B00110000,B00111100,B00001110,B00001110,B00111100,B11110000,B11000000,B00000000};
  byte writeIN[14]={B00000000,B11111110,B11111110,B00000000,B11111110,B11111110,B01100000,B00110000,B11111110,B11111110,B00000000,B11110110,B11110110,B00000000};
  
  for (int col=0; col<13; col++)
  {
    lc.setEyeColumn(1,col, writeW[col],false);
    lc.setEyeColumn(2,col, writeIN[col],false);
  }
  delay(1000);
  
  */
}
void sopalint()
{
 byte writeSopalint[48]={B11110110,B11010110,B11010110,B11011110,B11011110,B00000000,B11111110,B11111110,B11000110,B11111110,B11111110,B00000000,B11111110,B11111110,B11011000,B11011000,B11111000,B00000000,B11111110,B11111110,B11011000,B11111110,B11111110,B00000000,B11111110,B11111110,B00000110,B00000110,B00000110,B11000000,B00000000,B11111110,B11111110,B00000000,B11111110,B11111110,B01110000,B00111000,B11111110,B11111110,B00000000,B11000000,B11000000,B11111110,B11111110,B11000000,B11000000};
 int j;
for(int i=47 ; i>-29 ; i--) //Pas de d\u00e9filement
 {
      for(int col=0 ; col=28; col++)
     {
       if(i+col > 47)
       j = 5; // colonne vide
       else
       j = i+col;
       
       lc.setMatrixColumn(col,writeSopalint[j]);
     }
 }
}
void cardio()
{
  byte cardio[14]={B00010000,B00010000,B01100000,B10000000,B01111100,B00000010,B00011100,B00010000,B00010000,B00100000,B00010000,B00010000,B00010000,B00010000};
  
  //Affichage ligne
  for (int col=0 ; col<28 ; col++)
  {
    lc.setMatrixColumn(col,B00010000); //Ligne 
    lc.setMatrixColumn(col-10,B00000000); //Efface la ligne au fur et \u00e0 mesure
    delay(20);
  }
  //Supp fin de ligne
   for (int col=28-10 ; col<28 ; col++)
  {
    lc.setMatrixColumn(col,B00000000); //Efface la ligne
    delay(20);
  }
  //Affichage cardio
  for(int eye=1;eye<=2;eye++)
  {
    
     for (int col=0 ; col<14 ; col++)
    {
      lc.setEyeColumn(eye,col,cardio[col],false); //cardio
      delay(30);
      //lc.setEyeColumn(1,col,(byte)0,true); //cardio
    }
  }
}

void choukette()
{
  byte writeCho[14]={B01111100,B01000100,B01000100,B01000100,B00000000,B01111100,B00010000,B00010000,B01111100,B00000000,B01111100,B01000100,B01000100,B01111100};
  byte writeUk[14]={B01111100,B00000100,B00000100,B01111100,B00000000,B01111100,B00010000,B00101000,B01000100,B00010000,B00111000,B00011100,B00111000,B00010000};

  for (int col=0; col<=13; col++)
   {
       lc.setEyeColumn(1, col,  writeCho[col], false); 
       lc.setEyeColumn(2, col,  writeUk[col], false); 
   }
   delay(1000);

}
void loop() 
{ 
  
  gauchedroite();
  choukette();
  /*
  int j = 0;
  while(true)
 { 
    for(int i=0; i<5;i++)
    cylon();
    
    if(j%2 == 0)
    cardio();
    else
    emoticon(2);
    
    j++;
 }
 */
 
 /*/Bouquet final !
  for(int j=1 ; j<13 ; j++)
  {
    //for(int i=0; i<2 ; i++)
    gauchedroite();
    switch(j)
    {
      case 8 : 
      pacman();
      break;
      
      case 9 : 
      cercle();
      break;
      
      case 10 : 
      cardio();
      break;
      
      case 11: 
      balayageV();
      break;
      
      case 12: 
      cylon();
      break;
      
      default:
      emoticon(j);
      
    }
  }*/
}

