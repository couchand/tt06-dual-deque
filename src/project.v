/*
 * Copyright (c) 2024 Andrew Dona-Couch
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_couchand_dual_stack (
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output reg  [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  assign uio_out[3:0] = 4'b0;
  assign uio_oe = 8'b11110000;

  dual_stack dual_stack_instance (
    .clk(clk),
    .rst_n(rst_n),
    .s1_empty(uio_out[4]),
    .s1_full(uio_out[5]),
    .s2_empty(uio_out[6]),
    .s2_full(uio_out[7]),
    .stack_select(uio_in[0]),
    .push(uio_in[1]),
    .pop(uio_in[2]),
    .data_in(ui_in),
    .data_out(uo_out)
  );

endmodule
