/*
 * File:   serial.hpp
 * Author: philippe
 *
 * Created on 4 février 2012, 19:00
 */

#ifndef SERIAL_HPP
#define	SERIAL_HPP

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <string.h>
#include <libintech/singleton.hpp>
#include <stdint.h>

#define rx_buffer__SIZE 32

template<uint8_t id>
class Serial{
private:
    struct ring_buffer
    {
        ring_buffer(){
        }
        unsigned char buffer[rx_buffer__SIZE] ;
        int head;
        int tail;
    };

    static volatile ring_buffer rx_buffer_;

private:

    static void PLEASE_INCLUDE_SERIAL_INTERRUPT();


    static inline bool available(void)
    {
    		return (rx_buffer__SIZE + rx_buffer_.head - rx_buffer_.tail) % rx_buffer__SIZE;
    }

    static inline void send_ln(){
	send_char('\r');
    	send_char('\n');
    }


    static inline unsigned char read_single_char(){
    while(!available()){ asm("nop"); }
    unsigned char c = rx_buffer_.buffer[rx_buffer_.tail];
    rx_buffer_.tail = (rx_buffer_.tail + 1) % rx_buffer__SIZE;
    return c;
    }

public:

    static inline void init();

    static inline void change_baudrate(uint32_t BAUD_RATE);

    static inline void send_char(unsigned char byte);

    static inline void store_char(unsigned char c)
    {
    	int i = (rx_buffer_.head + 1) % rx_buffer__SIZE;
    	if (i != rx_buffer_.tail)
    	{
    		rx_buffer_.buffer[rx_buffer_.head] = c;
    		rx_buffer_.head = i;
    	}
    }

    template<class T>
    static inline void print_binary(T val){
        static char buff[sizeof(T) * 8 + 1];
	buff[sizeof(T) * 8]='\0';
        int16_t j = sizeof(T) * 8 - 1;
        for(int16_t i=0 ; i<sizeof(T)*8 ; ++i){
            if(val & ((T)1 << i))
               buff[j] = '1';
            else
               buff[j] = '0';
            j--;
        }
        print((const char *)buff);
    }

    static inline void print_binary(unsigned char * val, int16_t len){
        for(int16_t i = 0 ; i<len ; ++i){
		print_binary(val[i]);
	}
    }

    template<class T>
    static inline void print_noln(T val){
    	char buffer[10];
        ltoa(val,buffer,10);
    	print_noln((const char *)buffer);
    }

    static inline void print_noln(char val){
    	send_char(val);
    	send_char('\r');
    }

    static inline void print_noln(unsigned char val){
        send_char(val);
        send_char('\r');
    }

    static inline void print_noln(const char * val)
    {
    	for(uint16_t i = 0 ; i < strlen(val) ; i++)
    	{
    		send_char(val[i]);
    	}
    	send_char('\r');
    }

    template<class T>
    static inline void print(T val){
        print_noln(val);
        send_char('\n');
    }

    static inline int32_t read_int(void){
        static char buffer[20];
        buffer[read(buffer,20)] = '\0';
        return atol(buffer);
    }

    static inline uint32_t read_uint(void){
        static char buffer[20];
        buffer[read(buffer,20)] = '\0';
        return atol(buffer);
    }

    static inline float read_float(){
        static char buffer[20];
	buffer[read(buffer,20)] = '\0';
        return atof(buffer);
    }

    static inline unsigned char read_char(){
        unsigned char res = read_single_char();
        //Lecture \r
        read_single_char();
        return res;
    }

    static inline uint8_t read(unsigned char* string, uint8_t length){
    	uint8_t i = 0;
    	for (; i < length; i++){
        	unsigned char tmp = read_single_char();
        	if(tmp == '\r'){
        		return i;
		}
        	string[i] = tmp;
        }
        return i;
    }


    static inline uint8_t read(char* string, uint8_t length){
        uint8_t i = 0;
        for (; i < length; i++){
            while(!available()){ asm("nop"); }
            char tmp = static_cast<char>(read_single_char());
            if(tmp == '\r'){
                return i;
	    }
            string[i] = tmp;
        }
        return i;
    }
};


template<uint8_t ID>
volatile typename Serial<ID>::ring_buffer Serial<ID>::rx_buffer_;

#endif	/* SERIAL_HPP */


