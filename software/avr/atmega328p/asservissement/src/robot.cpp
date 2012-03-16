#include <math.h>
#define PI 3.14159265

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>


// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('r')
				,x_(0)
				,y_(0)
				,angle_courant_(0.0)
				,rotation_en_cours_(false)
				,translation_attendue_(false)
				,rotation_attendue_(false)
				,goto_attendu_(false)
				,etat_rot_(true)
				,etat_tra_(true)
				,demande_stop_(false)
				,translation(0.6,2,0.0)
				,rotation(1,3,0.0)
// 				,translation(0.6,3,0.01)
// 				,rotation(0.4,3,0.01)
				,CONVERSION_TIC_MM_(0.1061)
				,CONVERSION_TIC_RADIAN_(0.000737463064)
	
	
{
	TWI_init();
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::change_baudrate(9600);
}

void Robot::asservir(int32_t distance, int32_t angle)
{
	int32_t pwmTranslation;
	int32_t pwmRotation;
	
	if (etat_rot_)
		pwmRotation = rotation.pwm(angle);
	else
		pwmRotation = 0;
	
	if(etat_tra_)
		pwmTranslation = translation.pwm(distance);
	else
		pwmTranslation = 0;
	
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
}



void Robot::updatePosition(int32_t distance, int32_t angle)
{
    
	static int32_t last_distance = 0;
	static int32_t last_angle = 0;

	int16_t delta_distance_tic = distance - last_distance;
	int16_t delta_angle_tic = angle - last_angle;
	int32_t last_angle_abs;
    
	if(couleur_ == 'v')
		last_angle_abs= (last_angle + 4260);
	else
		last_angle_abs = last_angle;
		
	float last_angle_radian = last_angle_abs* CONVERSION_TIC_RADIAN_;
	float delta_distance_mm = delta_distance_tic * CONVERSION_TIC_MM_;
	x_ += ( delta_distance_mm * cos( last_angle_radian ) );
	y_ += ( delta_distance_mm * sin( last_angle_radian ) );
	
	
	angle_courant((float) angle_courant() + delta_angle_tic * CONVERSION_TIC_RADIAN_);
	
	last_distance = distance;
	
	last_angle = angle;
	
}

////////////////////////////// PROTOCOLE SERIE ///////////////////////////////////
void Robot::communiquer_pc(){
	char buffer[17];
	uint8_t length = serial_t_::read(buffer,17);

#define COMPARE_BUFFER(string) strncmp(buffer, string, length) == 0 && length>0

	if(COMPARE_BUFFER("?")){
		serial_t_::print(0);
	}

	else if(COMPARE_BUFFER("ccr")){
		couleur_ = 'r';
	}
	else if(COMPARE_BUFFER("ccv")){
		couleur_ = 'v';
	}
	
	else if(COMPARE_BUFFER("crp")){
		rotation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crd")){
		rotation.kd(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cri")){
		rotation.ki(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("ctp")){
		translation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("ctd")){
		translation.kd(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cti")){
		translation.ki(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("ctm")){
		translation.valeur_bridage(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crm")){
		rotation.valeur_bridage(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("cx")){
		x(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cy")){
		y(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("co")){
		angle_courant(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("ec")){
		serial_t_::print((char)couleur_);
	}
	
	else if(COMPARE_BUFFER("erp")){
		serial_t_::print(rotation.kp());
	}
	else if(COMPARE_BUFFER("erd")){
		serial_t_::print(rotation.kd());
	}
	else if(COMPARE_BUFFER("eri")){
		serial_t_::print(rotation.ki());
	}
	else if(COMPARE_BUFFER("erm")){
		serial_t_::print(rotation.valeur_bridage());
	}

	else if(COMPARE_BUFFER("etp")){
		serial_t_::print(translation.kp());
	}
	else if(COMPARE_BUFFER("etd")){
		serial_t_::print(translation.kd());
	}
	else if(COMPARE_BUFFER("eti")){
		serial_t_::print(translation.ki());
	}
	else if(COMPARE_BUFFER("etm")){
		serial_t_::print(translation.valeur_bridage());
	}
	
	else if(COMPARE_BUFFER("ex")){
		serial_t_::print((int32_t)x());
	}
	else if(COMPARE_BUFFER("ey")){
		serial_t_::print((int32_t)y());
	}
	else if(COMPARE_BUFFER("eo")){
		serial_t_::print((int32_t)((float)angle_courant()*1000));
	}
	
	else if(COMPARE_BUFFER("d")){
		debut_translater(serial_t_::read_float());
		rotation_en_cours_ = true;
	}
	else if(COMPARE_BUFFER("t")){
		debut_tourner(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("goto")){
		float co_x = serial_t_::read_float();
		float co_y = serial_t_::read_float();      
		gotoPos(co_x , co_y);
	}
	
	else if(COMPARE_BUFFER("stop")){
		demande_stop_ = true;
	}
	
	//stopper asservissement rotation/translation
	else if(COMPARE_BUFFER("cr0")){
		etat_rot_ = false;
	}
	else if(COMPARE_BUFFER("ct0")){
		etat_tra_ = false;
	}
	
	//démarrer asservissement rotation/translation
	else if(COMPARE_BUFFER("cr1")){
		etat_rot_ = true;
	}
	else if(COMPARE_BUFFER("ct1")){
		etat_tra_ = true;
	}

#undef COMPARE_BUFFER
}


////////////////////////////// ACCESSEURS /////////////////////////////////

unsigned char Robot::couleur(void)
{
return couleur_;
}

void Robot::couleur(unsigned char couleur)
{ 
	if (couleur == 'r' || couleur == 'v')
		couleur_ = couleur;
}

float Robot::x(void)
{
return (float)x_;
}

void Robot::x(float new_x)
{
	x_ = new_x;
}

float Robot::y(void)
{
return (float)y_;
}

void Robot::y(float new_y)
{
	y_ = new_y;
}

float Robot::angle_courant(void)
{
return (float)angle_courant_;
}

void Robot::angle_courant(float new_angle)
{
	angle_courant_ = new_angle;
}

////////////////////////////// DEPLACEMENTS ET STOPPAGE ///////////////////////////////////
	

void Robot::gotoPos(float x, float y)
{
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	float angle;
	angle=atan2(delta_y,delta_x);
	goto_attendu_ = true;
	debut_tourner(angle);
	debut_translater(sqrt(delta_x*delta_x+delta_y*delta_y));
	
}



void Robot::debut_tourner(float angle)
{
	static float angleBkp = 4260;
// 	static float angleBkp = ((couleur_ == 'v') ? 4260 : 0);
	rotation_attendue_ = true;
	float ang1 = abs(angle-angleBkp);
	float ang2 = abs(angle+2*PI-angleBkp);
	float ang3 = abs(angle-2*PI-angleBkp);
    
	if (!(ang1 < ang2 && ang1 < ang3))
	{
		if (ang2 < ang3)
			angle += 2*PI;
		else
			angle -=  2*PI;
	}
	angleBkp=angle;
    
	rotation.consigne(angle/CONVERSION_TIC_RADIAN_);
}
	
	
	
void Robot::fin_tourner()
{
	if (consigne_tra_ != translation.consigne())
		translation.consigne(consigne_tra_);
	else if (rotation_attendue_)
	{
		rotation_attendue_ = false;
		if (not goto_attendu_)
			Serial<0>::print("FIN_TOU");
		else
		{
			goto_attendu_ = false;
			Serial<0>::print("FIN_GOTO");
		}
	}
}

void Robot::debut_translater(float distance)
{	
	translation_attendue_ = true;
	consigne_tra_ = translation.consigne()+distance/CONVERSION_TIC_MM_;
}


void Robot::fin_translater()
{
	if (translation_attendue_)
	{
		translation_attendue_ = false;
		if (not goto_attendu_)
			Serial<0>::print("FIN_TRA");
	}
}

void Robot::stopper(int32_t distance)
{
	demande_stop_ = false;
	
	//stop en rotation. risque de tour sur lui meme ? (probleme +/- 2pi)
	rotation.consigne(angle_courant()/CONVERSION_TIC_RADIAN_);
	//stop en translation
	consigne_tra_ = distance;
	translation.consigne(distance);
}

void Robot::atteinteConsignes()
{
	static bool translation_en_cours = false;
	
	if (abs(rotation.pwmCourant())>=10)
		rotation_en_cours_ = true;

	if (rotation_en_cours_ && abs(rotation.pwmCourant())<10)
	{
		
		rotation_en_cours_ = false;
		fin_tourner();
	}
	
	if (abs(translation.pwmCourant())>=10)
		translation_en_cours = true;

	if (translation_en_cours && abs(translation.pwmCourant())<10)
	{
		translation_en_cours = false;
		fin_translater();
	}
}

void Robot::gestionStoppage(int32_t distance, int32_t angle)
{
	
	static float compteurBlocage=0;
	static int32_t last_distance;
	static int32_t last_angle;
	
	//gestion de l'arret
	if (demande_stop_)
		stopper(distance);

	//detection d'un blocage - translation	
	if (	   abs(rotation.pwmCourant())>0 
		&& abs(translation.pwmCourant())>0 
		&& abs(last_distance-distance)<10
		&& abs(last_angle-angle)<10
	   )
	{
			
		if(compteurBlocage==20){
// 			demande_stop_ = true;
			stopper(distance);
			compteurBlocage=0;
		}
		else{
			compteurBlocage++;
		}
		
	}
	else
	{
		compteurBlocage=0;
	}
	
	
	last_distance = distance;
	last_angle = angle;
}
