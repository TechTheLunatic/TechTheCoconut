#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_1_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/serial/serial_1.hpp>
#include <libintech/timer.hpp>

#include <stdint.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "balise.h"
#include "frame.h"
#include "crc8.h"
#include "utils.h"

//Fonctions de modifications de bits
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif

#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif

#ifndef tbi
#define tbi(port,bit) (port) ^= (1 << (bit))
#endif

#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

#define READ_CANAL_A() rbi(PINB,PORTB4)
#define READ_CANAL_B() rbi(PINB,PORTB5)

void init();

volatile uint8_t dernier_etat_a;
volatile uint8_t dernier_etat_b;
volatile int32_t codeur;
volatile int32_t last_codeur = 0;

int main() {
	Balise & balise = Balise::Instance();
	init();
	uint32_t rawFrame=0;
	balise.moteur_on();
	Balise::serial_pc::print("init");
	while (1) {
		char buffer[10];
		Balise::Balise::serial_pc::read(buffer,10);
		
		#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

		if(COMPARE_BUFFER("?",1)){
// 			Balise::serial_pc::print(Balise::T_TopTour::value());
			Balise::serial_pc::print(2);
		}
		
		if(COMPARE_BUFFER("!",1)){
			Balise::serial_radio::print_noln('?');
// 			char buffer[10] = {0};
// 			Balise::Balise::serial_radio::read(buffer,10);
			Balise::serial_pc::print(Balise::serial_radio::read_int());
		}
		
		if(COMPARE_BUFFER("v",1)){
			bool is_valid = false;
// 			Frame frame = 0;
			int16_t n_demandes = 0;
			int32_t distance;
			int32_t offset = 0;
			int32_t angle = 0;
			int32_t crc = 0;
			do{
				Balise::serial_radio::print_noln('v');
				
				//Calcul du temps des read pour correction de l'offset
				int32_t t1 = Balise::T_TopTour::value();
				distance = Balise::serial_radio::read_int();
				offset = Balise::serial_radio::read_int();
// 				crc = Balise::serial_radio::read_int();
				int32_t t2 = Balise::T_TopTour::value();			
				
				if(t2 < t1){
				  t2+=balise.max_counter();
				}
				angle = balise.getAngle(offset + (t2 - t1)*5/4);
				
// 				is_valid = (crc==crc8((distance << 16) + offset));
				is_valid = true;
				n_demandes++;
			}while(is_valid==false && n_demandes<5);
			if(n_demandes==5){
				Balise::serial_pc::print("ERREUR_CANAL");
			}
			else if(distance==0){
				//Distance écrasée par le timeout côté balise (distance périmée).
				Balise::serial_pc::print("NON"); 
			}
			else{
				char str[80] = {0};
				char buff[20];
// 				Balise::serial_pc::print(offset);
				ltoa(1,buff,10);
				strcat(str,buff);
				strcat(str,".");
				ltoa(distance,buff,10);
				strcat(str,buff);
				strcat(str,".");
				ltoa(angle,buff,10);
				strcat(str,buff);
				Balise::serial_pc::print((const char *)str);
			}
		}
		#undef COMPARE_BUFFER*/
	}
	
}

void init()
{
	
	//5V sur la pin 12 (B6) pour la direction laser
	sbi(DDRB,PORTB6);
	sbi(PORTB,PORTB6);
	//On met la pin 13 (OC0A, B7) en OUT
	sbi(DDRB,PORTB7);

	//Config PWM de la pin 13 (créneau de 40Hz)
	//Active mode CTC (cf datasheet p 96)
	cbi(TCCR0A,WGM00);
	sbi(TCCR0A,WGM01);
	cbi(TCCR0B,WGM02);
	//Défini le mode de comparaison
	sbi(TCCR0A,COM0A0);
	cbi(TCCR0A,COM0A1);
	// Prescaler (=1)
	cbi(TCCR0B,CS02);
	cbi(TCCR0B,CS01);
	sbi(TCCR0B,CS00);
	//Seuil (cf formule datasheet)
	//f_wanted=16000000/(2*prescaler*(1+OCR0A))
	OCR0A= 120;
	
	//Initialisation table pour crc8
	init_crc8();
 	
 	//Pin21 = input impulsion compte tour
	//Activation des interruptions sur front montant pour pin 21 sur board Arduino
	sbi(EICRA,ISC01);//Configuration front montant
	sbi(EICRA,ISC00);
	sbi(EIMSK,INT0);//Activation proprement dite

	// Initialisation interruptions codeurs
	// Interruptions de codeuse(PCINT4 => Pin 10 sur l'Arduino)
	sbi(PCMSK0,PCINT4);
	// Activer les interruptions
	sbi(PCICR,PCIE0);

	// Initialisation interruptions codeurs
	// Masques
	//PCMSK0 |= (1 << PCINT7);
	// Activer les interruptions
	//PCICR |= (1 << PCIE0);
	
// 	sei();
}

ISR(TIMER1_OVF_vect)
{
	//Serial<0>::print(codeur - last_codeur);
	Balise::Instance().asservir(codeur - last_codeur);
	last_codeur = codeur;
}

ISR(TIMER3_OVF_vect)
{
// 	Balise::serial_pc::print(12);
// 	Balise::Instance().incremente_toptour();
// 	Balise::Instance().asservir(codeur - last_codeur);
}

//INT0
ISR(INT0_vect)
{
	Balise & balise = Balise::Instance();
	if(Balise::T_TopTour::value()>=30){
		balise.max_counter(Balise::T_TopTour::value());
		Balise::T_TopTour::value(0);
	}
}

ISR(PCINT0_vect)
{
	 if(dernier_etat_a == 0 && READ_CANAL_A() == 1){
	   if(READ_CANAL_B() == 0)
	     codeur--;
	   else
	     codeur++;
	 }
	 else if(dernier_etat_a == 1 && READ_CANAL_A() == 0){
	   if(READ_CANAL_B() == 0)
	     codeur++;
	   else
	     codeur--;
	 }
	 else if(dernier_etat_b == 0 && READ_CANAL_B() == 1){
	   if(READ_CANAL_A() == 0)
	     codeur--;
	   else
	     codeur++;
	 }
	 else if(dernier_etat_b == 1 && READ_CANAL_B() == 0){
	   if(READ_CANAL_A() == 0)
	     codeur++;
	   else
	     codeur--;
	 }
	dernier_etat_a = READ_CANAL_A();
	dernier_etat_b = READ_CANAL_B(); 
}
