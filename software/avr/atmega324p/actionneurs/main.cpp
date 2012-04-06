#include <util/delay.h>
#include "ax12.h"
#include "actionneurs.h"



// #define FLASH_ID_MODE
// #define FLASH_BAUD_RATE_MODE
#define TEST_NOSERIE_MODE
#define REANIMATION_MODE

#include "serial.h"

#include <avr/io.h>
#include <avr/interrupt.h>


int main()
{
    uart_init();
    // REANIMATION_MODE :
    #ifdef REANIMATION_MODE
        byte debug_baudrate = 0x00;
    #endif
        
    // BAUD RATE de la série (envoi)
    ax12Init(BAUD_RATE_SERIE);
    
    #ifdef FLASH_BAUD_RATE_MODE
        // BAUD RATE de l'AX12 (réception)
        writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
    #endif
        
    #ifdef FLASH_ID_MODE
        AX12InitID(3);
    #endif
        
    // Initialisation de tous les AX12
    AX12Init (AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
        
    while (1)
    {
        
        #ifdef REANIMATION_MODE
            
            ax12Init(2000000/(debug_baudrate + 1));
            
            debug_baudrate++;
        #endif       
        
        #ifdef TEST_NOSERIE_MODE 
            AX12Init(0xFE, 0,0,200);
        #else
            
        if (available())
        {
                
                unsigned char packet = read();
                char consigne;
                extraction_consigne(packet, &consigne);
                
                // ROTATION DE l'AX12
                if (consigne == 0)
                {
                    char id;
                    char angle;
                    extraction(packet, &id, &angle);                
                    AX12GoTo(id, 198 +  angle*627/31);
                }
                
                // ORDRE A DONNER A L'AX12
                else
                {
                    char ordre;
                    char valeur;
                    extraction(packet, &ordre, &valeur);
                    
                    // CHANGER LA VITESSE
                    if (ordre == 0)
                        AX12Init(AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW, valeur*500/31);
                    
                    
                    // CHANGEMENT DE l'ID
                    else if (ordre == 1)
                        AX12InitID(valeur);
                    
                    // CHANGEMENT DU BAUD RATE
                    else if (ordre == 2)
                    {
                        if (valeur == 0)
                            writeData(AX_BROADCAST, AX_BAUD_RATE, 1, AX_BAUD_RATE_1000000);
                        else if (valeur == 1)
                            writeData(AX_BROADCAST, AX_BAUD_RATE, 1, AX_BAUD_RATE_200000);
                        else if (valeur == 2)
                            writeData(AX_BROADCAST, AX_BAUD_RATE, 1, AX_BAUD_RATE_115200);
                        else if (valeur == 3)
                            writeData(AX_BROADCAST, AX_BAUD_RATE, 1, AX_BAUD_RATE_57600);
                        else if (valeur == 4)
                            writeData(AX_BROADCAST, AX_BAUD_RATE, 1, AX_BAUD_RATE_9600);
                    }   
                }   
        }
        #endif
// 
    }
    return 0;
}
