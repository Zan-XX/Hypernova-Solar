#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "conv.h"

uint8_t * intToByteArr(unsigned int x) {
	static uint8_t  output[int_len];
	for (int i = 0;i < int_len;i++) {
		uint8_t tmp = x >> (8 * i);
		output[int_len - (i + 1)] = tmp;
	}
	return output;
}

unsigned int byteArrToInt(uint8_t x[]) {
	static unsigned int y;
	for(int i = 0;i < int_len;i++) {
		y = (y << 8) | x[i];
	}
	return y;
}
