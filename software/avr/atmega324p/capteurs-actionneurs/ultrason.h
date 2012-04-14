#ifndef ULTRASON_HPP
#define ULTRASON_HPP

#include <libintech/timer.hpp>
#include <libintech/register.hpp>
#include <libintech/ring_buffer.hpp>

int compare (const void * a, const void * b);
  
template<class Timer, class Pin>
class ultrason
{
  static const int size = 3;
  typedef uint16_t mesure_t;
  ring_buffer<mesure_t, size> mesures_;
  uint16_t derniere_valeur_;

  void bubbleSort(mesure_t* array)
{
    int i,j;
    for(i=0;i<size;i++)
    {
        for(j=0;j<i;j++)
        {
            if(array[i]>array[j])
            {
                int temp=array[i];
                array[i]=array[j];
                array[j]=temp;
            }

        }

    }
}

public:
  ultrason(){
    Timer::init();
  }
  
  void update(){
    if(Pin::read()){
		derniere_valeur_ = Timer::value();
    }else{//Front descendant
	// prescaler/fcpu*inchToCm/tempsParInch
	if(Timer::value() <derniere_valeur_)
	  mesures_.append((Timer::value() + 65536 - derniere_valeur_  )*0.0884353741496);
	else
	  mesures_.append((Timer::value() - derniere_valeur_ )*0.0884353741496);
    }
  }
  
  uint16_t mediane(){
    bubbleSort(mesures_.data());
    return mesures_.data()[mesures_.size()/2];
  }
  
};

extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD2> > ultrason_g;
extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD3> > ultrason_d;

#endif