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

  assign full = (front_wr == ((back_wr + 1) % WORDS)) & ~empty;

  assign data_out = empty | ~ds ? 0
    : es ? DEQUE[back_rd] : DEQUE[front_rd];

  always @(posedge clk) begin
    if (!rst_n) begin
      empty <= 1;
      front_wr <= 0;
      back_wr <= WORDS - 1;
      ds <= 0;
      es <= 0;
      for (int i = 0; i < WORDS; i++) begin
        DEQUE[i] <= 8'b0;
      end
    end else if (deque_select == ADDR) begin
      ds <= 1;
      es <= end_select;
      if (push & pop) begin
        if (~empty) begin
          if (end_select) begin
            DEQUE[back_rd] <= data_in;
          end else begin
             DEQUE[front_rd] <= data_in;
          end
        end
      end else if (push) begin
        if (~full) begin
          empty <= 0;
          if (end_select) begin
            DEQUE[back_wr] <= data_in;
            back_wr <= back_wr == 0 ? WORDS - 1 : back_wr - 1;
          end else begin
            DEQUE[front_wr] <= data_in;
            front_wr <= front_wr == WORDS - 1 ? 0 : front_wr + 1;
          end
        end
      end else if (pop) begin
        if (~empty) begin
          if (end_select) begin
            back_wr <= back_rd;
            if (back_rd == front_rd) begin
              empty <= 1;
            end
          end else begin
            front_wr <= front_rd;
            if (front_rd == back_rd) begin
              empty <= 1;
            end
          end
        end
      end
    end else begin
      ds <= 0;
      es <= end_select;
    end
  end

endmodule
