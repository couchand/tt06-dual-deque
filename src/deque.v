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
    input  wire       end_select,
    input  wire       push,
    input  wire       pop,
    input  wire [7:0] data_in,
    output wire [7:0] data_out
);

  localparam addr_bits = $clog2(WORDS);

  reg [addr_bits-1:0] front_wr, back_wr;
  reg [7:0] DEQUE[WORDS - 1:0];
  reg ds, es;

  wire [addr_bits-1:0] front_rd = front_wr != 0 ? front_wr - 1 : WORDS - 1;
  wire [addr_bits-1:0] back_rd = back_wr != WORDS - 1 ? back_wr + 1 : 0;

  assign full = front_wr == back_wr & ~empty;

  wire [addr_bits-1:0] addr_wr = es ? back_wr : front_wr;
  wire [addr_bits-1:0] addr_rd = es ? back_rd : front_rd;
  assign data_out = empty | ~ds ? 0 : DEQUE[addr_rd];

  always @(posedge clk) begin
    if (!rst_n) begin
      empty <= 1;
      front_wr <= 0;
      back_wr <= 0;
      ds <= 0;
      es <= 0;
      for (int i = 0; i < WORDS; i++) begin
        DEQUE[i] <= 8'b0;
      end
    end else if (deque_select == ADDR) begin
      ds <= 1;
      es <= end_select;
      if (push & pop & ~empty) begin
        DEQUE[addr_rd] <= data_in;
      end else if (push & ~full) begin
        DEQUE[addr_wr] <= data_in;
        empty <= 0;
        if (es) begin
          back_wr <= back_wr == 0 ? WORDS : back_wr - 1;
        end else begin
          front_wr <= front_wr == WORDS - 1 ? 0 : front_wr + 1;
        end
      end else if (pop & ~empty) begin
        if (es) begin
          back_wr <= back_rd;
          if (back_rd == front_wr) begin
            empty <= 1;
          end
        end else begin
          front_wr <= front_rd;
          if (front_rd == back_wr) begin
            empty <= 1;
          end
        end
      end
    end else begin
      ds <= 0;
      es <= end_select;
    end
  end

endmodule
