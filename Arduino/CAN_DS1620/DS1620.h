/*
Copyright (c) 2011, Matt Sparks
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
*/

/* Inspired by a similar library by Ruben Laguna. */

#ifndef DS1620_h
#define DS1620_h

#include <math.h>
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WConstants.h"
#endif


class DS1620
{
 public:
  /**
   * Interface with a DS1620 chip.
   *
   * Args:
   *   rst: RST pin number
   *   clk: CLK pin number
   *   dq: DQ pin number
   */
  DS1620(int rst, int clk, int dq);

  /**
   * Set up the DS1620 in CPU mode with 1-shot mode enabled.
   */
  void config();

  /**
   * Get the current temperature reading in Celsius.
   *
   * Returns:
   *   temperature in degrees Celcius.
   */
  float temp_c();

 private:
  const int rst_pin_;
  const int clk_pin_;
  const int dq_pin_;

  enum DataSize {
    eight_bits_,
    nine_bits_
  };

  /**
   * Command constants.
   *
   * Many of these are supported by the DS1602, but are unused in this library.
   */
  enum Command {
    read_temp_    = 0xAA,
    write_th_     = 0x01,
    write_tl_     = 0x02,
    read_th_      = 0xA1,
    read_tl_      = 0xA2,
    read_cnt_     = 0xA0,
    read_slope_   = 0xA9,
    start_conv_   = 0xEE,
    stop_conv_    = 0x22,
    write_config_ = 0x0C,
    read_config_  = 0xAC
  };

  /**
   * Sets the pin levels to prepare for reading and writing.
   */
  void start_transfer();
  /**
   * Resets pin levels after communication.
   */
  void end_transfer();

  /**
   * Trigger a temperature conversion in 1-shot mode, or enable continuous
   * conversion.
   */
  void start_conv();
  /**
   * Disable continuous conversion.
   */
  void stop_conv();

  /**
   * Read data from the DS1602.
   *
   * start_transfer() must be called before using this function.
   */
  word read_data(DataSize size);

  /**
   * Write data to the DS1602.
   *
   * start_transfer() must be called before using this function.
   */
  void write_data(word data, DataSize size);

  /**
   * Higher-level functions used to write commands, possibly with arguments.
   *
   * start_transfer() does not need to be called before using this functions.
   */
  void write_command(Command command);
  void write_command_8bit(Command command, byte value);
};

#endif
