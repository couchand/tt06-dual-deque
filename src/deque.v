/*
 * Copyright (c) 2024 Andrew Dona-Couch
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module deque #(
    parameter ADDR = 0,
    parameter WORDS = 16
) (
    input  wire       clk,
    input  wire       rst_n,
    output reg        empty,
    output wire       full,
    input  wire       deque_select,
    input  wire       push,
    input  wire       pop,
    input  wire [7:0] data_in,
    output wire [7:0] data_out
);

  localparam addr_bits = $clog2(WORDS);

  reg [addr_bits-1:0] addr_wr;
  reg [7:0] DEQUE[WORDS - 1:0];
  reg ss;

  wire [addr_bits-1:0] addr_rd = addr_wr - 1;

  assign full = addr_rd == WORDS - 1 & ~empty;
  assign data_out = empty | ~ss ? 0 : DEQUE[addr_rd];

  always @(posedge clk) begin
    if (!rst_n) begin
      empty <= 1;
      addr_wr <= 0;
      ss <= 0;
      for (int i = 0; i < WORDS; i++) begin
        DEQUE[i] <= 8'b0;
      end
    end else if (deque_select == ADDR) begin
      ss <= 1;
      if (push & pop & ~empty) begin
        DEQUE[addr_rd] <= data_in;
      end else if (push & ~full) begin
        DEQUE[addr_wr] <= data_in;
        addr_wr <= addr_wr + 1;
        empty <= 0;
      end else if (pop & ~empty) begin
        addr_wr <= addr_rd;
        if (addr_rd == 0) begin
          empty <= 1;
        end
      end
    end else begin
      ss <= 0;
    end
  end

endmodule
