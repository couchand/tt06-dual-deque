# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_stacks(dut):
  dut._log.info("Start")

  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  # Initialization
  dut._log.info("Initialization")

  # Both empty at start
  assert dut.uio_out.value & 0xF0 == 0x50

  # Data lines are zero when empty

  # Stack 0
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0

  # Stack 1
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0


  # Push
  dut._log.info("Push")

  ## Stack 0
  dut.ui_in.value = 0x42
  dut.uio_in.value = 2
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)

  assert dut.uo_out.value == 0x42

  # Only stack 1 empty now
  assert dut.uio_out.value & 0xF0 == 0x40

  for i in range(1, 15):
    dut.ui_in.value = i
    dut.uio_in.value = 2
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x40

  dut.ui_in.value = 0x9F
  dut.uio_in.value = 2
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x9F

  # Now stack 0 full
  assert dut.uio_out.value & 0xF0 == 0x60

  ## Stack 1
  dut.ui_in.value = 0x42
  dut.uio_in.value = 3
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)

  assert dut.uo_out.value == 0x42

  # Stack 1 no longer empty
  assert dut.uio_out.value & 0xF0 == 0x20

  for i in range(1, 15):
    dut.ui_in.value = i
    dut.uio_in.value = 3
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x20

  dut.ui_in.value = 0x9F
  dut.uio_in.value = 3
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x9F

  # Now stack 1 full, too
  assert dut.uio_out.value & 0xF0 == 0xA0

  # Pop
  dut._log.info("Pop")

  dut.uio_in.value = 4
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 5
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)

  assert dut.uio_out.value & 0xF0 == 0x00

  for i in range(14, 0, -1):
    dut.uio_in.value = 4
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x00

    dut.uio_in.value = 5
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x00

    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)

  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x42
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x42

  dut.uio_in.value = 4
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 5
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)

  # Both empty again
  assert dut.uio_out.value & 0xF0 == 0x50

  await ClockCycles(dut.clk, 10)
  dut._log.info("Tests pass")
