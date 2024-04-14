/*
 * Copyright (c) 2024 Andrew Dona-Couch
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module dual_deque (
    input  wire       clk,
    input  wire       rst_n,
    output wire       s0_empty,
    output wire       s0_full,
    output wire       s1_empty,
    output wire       s1_full,
    input  wire       deque_select,
    input  wire       push,
    input  wire       pop,
    input  wire [7:0] data_in,
    output wire [7:0] data_out
);

  wire [7:0] s0_out, s1_out;
  assign data_out = s0_out | s1_out;

  deque #(
    .ADDR(0),
    .WORDS(16)
  ) deque0 (
    .clk(clk),
    .rst_n(rst_n),
    .empty(s0_empty),
    .full(s0_full),
    .deque_select(deque_select),
    .push(push),
    .pop(pop),
    .data_in(data_in),
    .data_out(s0_out)
  );

  deque #(
    .ADDR(1),
    .WORDS(16)
  ) deque1 (
    .clk(clk),
    .rst_n(rst_n),
    .empty(s1_empty),
    .full(s1_full),
    .deque_select(deque_select),
    .push(push),
    .pop(pop),
    .data_in(data_in),
    .data_out(s1_out)
  );

endmodule
