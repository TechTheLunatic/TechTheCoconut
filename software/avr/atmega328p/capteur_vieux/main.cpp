// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/capteur_vieux.hpp>

typedef Serial<0> serial_t_;
typedef Timer<1,ModeCounter,256> timerCapteur;

// typedef capteur_vieux<PORTD, PORTD6, timerCapteur, serial_t_>;

int main()
{
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    capteur_srf05::init();
    
    while(1) 
    {
            capteur_srf05::value();
            _delay_ms(100);
    }

    
    return 0;
}

// Interruption pour le timer1
ISR(TIMER1_OVF_vect)
{
    
}

