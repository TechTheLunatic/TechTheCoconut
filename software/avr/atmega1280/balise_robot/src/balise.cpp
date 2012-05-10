/**
 * \file balise.cpp
 */
#include "balise.h"
#include <libintech/serial/serial_0.hpp>
#include <libintech/serial/serial_1.hpp>

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}

uint16_t Balise::max_counter(){
	return max_counter_;
}

int16_t Balise::getAngle(uint16_t offset) {
	if(max_counter_==0)
	  return -1;
	
	//temps à soustraire de l'angle pour avoir la valeur au moment du passage du laser
	int32_t diff = ((int32_t)Balise::T_TopTour::value() - (int32_t)offset*4/5);
		
	while(diff<0){ //Assez mystère...
	  diff+=(int32_t)max_counter_;
	}

	return diff *(float)360/(float)max_counter_ ;

}

Balise::Balise() : asservissement_moteur_(0.5,0.5,0)
{
	asservissement_moteur_.consigne(0);
	serial_pc::init();
	serial_pc::change_baudrate(9600);
	serial_radio::init();
	serial_radio::change_baudrate(9600);
	T_Asservissement::init();
	T_TopTour::init();
	sei();
}

void Balise::asservir(int32_t vitesse_courante)
{
	int16_t pwm = asservissement_moteur_.pwm(vitesse_courante);
// 	Serial<0>::print(pwm);
	moteur_.envoyerPwm(pwm);
}

