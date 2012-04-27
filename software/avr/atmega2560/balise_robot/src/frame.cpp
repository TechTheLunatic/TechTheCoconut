/**
 * \file frame.cpp
 */

#include "frame.h"
#include <libintech/serial/serial_0.hpp>

Frame::Frame(uint32_t rawFrame) {
	 
	distance_ = (uint16_t) (rawFrame >> 20);//12 bits de poids les plus forts
	offset_ = ((uint16_t) (rawFrame >> 8)) && 0b0000111111111111 ;//12 bits entre
	crc_ = (uint8_t) (rawFrame);//8 bits de poids les plus faible	
}

bool Frame::isValid() {
	return (crc8(data_)==crc_);
}

uint16_t Frame::getDistance() {
	return distance_;
}

uint16_t Frame::getOffset() {
	return offset_;
}

uint8_t Frame::getCrc() {
	return crc_;
}
