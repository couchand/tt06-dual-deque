/*
 * Copyright (c) 2024 Andrew Dona-Couch
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module dual_deque (
    input  wire       clk,
    input  wire       rst_n,
    output wire       d0_empty,
    output wire       d0_full,
    output wire       d1_empty,
    output wire       d1_full,
    input  wire       deque_select,
    input  wire       end_select,
    input  wire       push,
    input  wire       pop,
    input  wire [7:0] data_in,
    output wire [7:0] data_out
);

  wire [7:0] d0_out, d1_out;
  assign data_out = d0_out | d1_out;

  deque #(
    .ADDR(0),
    .WORDS(16)
  ) deque0 (
    .clk(clk),
    .rst_n(rst_n),
    .empty(d0_empty),
    .full(d0_full),
    .deque_select(deque_select),
    .end_select(end_select),
    .push(push),
    .pop(pop),
    .data_in(data_in),
    .data_out(d0_out)
  );

  deque #(
    .ADDR(1),
    .WORDS(8)
  ) deque1 (
    .clk(clk),
    .rst_n(rst_n),
    .empty(d1_empty),
    .full(d1_full),
    .deque_select(deque_select),
    .end_select(end_select),
    .push(push),
    .pop(pop),
    .data_in(data_in),
    .data_out(d1_out)
  );

endmodule
