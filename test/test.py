# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import random

S0_SIZE = 16
S1_SIZE = 8

@cocotb.test()
async def test_queues(dut):
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

  # Queue 0
  dut._log.info("Push")
  dut.ui_in.value = 0x42
  dut.uio_in.value = 4
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x42

  # Only stack 1 empty now
  assert dut.uio_out.value & 0xF0 == 0x40

  dut.ui_in.value = 0xAB
  dut.uio_in.value = 4
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0xAB

  dut.uio_in.value = 2
  await ClockCycles(dut.clk, 2)
  assert dut.uo_out.value == 0x42

  dut.uio_in.value = 0xA
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0xAB

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
  dut.uio_in.value = 4
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)

  assert dut.uo_out.value == 0x42

  # Only stack 1 empty now
  assert dut.uio_out.value & 0xF0 == 0x40

  for i in range(1, S0_SIZE - 1):
    dut.ui_in.value = i
    dut.uio_in.value = 4
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x40

  dut.ui_in.value = 0x9F
  dut.uio_in.value = 4
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x9F

  # Now stack 0 full
  assert dut.uio_out.value & 0xF0 == 0x60

  # Try replacement
  dut.ui_in.value = 0x81
  dut.uio_in.value = 12
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x81
  assert dut.uio_out.value & 0xF0 == 0x60

  ## Stack 1
  dut.ui_in.value = 0x42
  dut.uio_in.value = 5
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)

  assert dut.uo_out.value == 0x42

  # Stack 1 no longer empty
  assert dut.uio_out.value & 0xF0 == 0x20

  for i in range(1, S1_SIZE - 1):
    dut.ui_in.value = i
    dut.uio_in.value = 5
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x20

  dut.ui_in.value = 0x9F
  dut.uio_in.value = 5
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x9F

  # Now stack 1 full, too
  assert dut.uio_out.value & 0xF0 == 0xA0

  # Try replacement
  dut.ui_in.value = 0x81
  dut.uio_in.value = 13
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x81
  assert dut.uio_out.value & 0xF0 == 0xA0

  # Pop
  dut._log.info("Pop")

  dut.uio_in.value = 8
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)

  assert dut.uio_out.value & 0xF0 == 0x80

  for i in range(S0_SIZE - 2, 0, -1):
    dut.uio_in.value = 8
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x80

    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)

  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x42

  dut.uio_in.value = 8
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1)

  # Now Stack 0 empty, Stack 1 Full
  assert dut.uio_out.value & 0xF0 == 0x90

  dut.uio_in.value = 9
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)

  assert dut.uio_out.value & 0xF0 == 0x10

  for i in range(S1_SIZE - 2, 0, -1):
    dut.uio_in.value = 9
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == i
    assert dut.uio_out.value & 0xF0 == 0x10

    dut.uio_in.value = 1
    await ClockCycles(dut.clk, 1)

  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)
  assert dut.uo_out.value == 0x42

  dut.uio_in.value = 9
  await ClockCycles(dut.clk, 1)
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 1)

  # Both empty again
  assert dut.uio_out.value & 0xF0 == 0x50

  await ClockCycles(dut.clk, 10)
  dut._log.info("Tests pass")

@cocotb.test()
async def test_fuzz(dut):
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
  await ClockCycles(dut.clk, 10)

  ss = 0
  s0 = []
  s1 = []

  for step in range(0, 4096):
    await ClockCycles(dut.clk, 1)

    #dut._log.info(f's0 {s0}')
    #dut._log.info(f's1 {s1}')

    if len(s0) == 0:
      assert dut.uio_out.value & 0x30 == 0x10
    elif len(s0) == S0_SIZE:
      assert dut.uio_out.value & 0x30 == 0x20
    else:
      assert dut.uio_out.value & 0x30 == 0x00

    if ss == 0:
      if len(s0) == 0:
        assert dut.uo_out.value == 0
      else:
        assert dut.uo_out.value == s0[len(s0) - 1]

    if len(s1) == 0:
      assert dut.uio_out.value & 0xC0 == 0x40
    elif len(s1) == S1_SIZE:
      assert dut.uio_out.value & 0xC0 == 0x80
    else:
      assert dut.uio_out.value & 0xC0 == 0x00

    if ss == 1:
      if len(s1) == 0:
        assert dut.uo_out.value == 0
      else:
        assert dut.uo_out.value == s1[len(s1) - 1]

    options = [
      'nop',
      'pushf0',
      'pushb0',
      'pushf1',
      'pushb1',
      'popf0',
      'popb0',
      'popf1',
      'popb1',
      'replacef0',
      'replaceb0',
      'replacef1',
      'replaceb1',
      'toggle',
    ]
    choice = random.choice(options)
    nextval = random.randrange(0, 256)
    #dut._log.info(f'{choice} {nextval}')

    if choice == 'pushf0':
      if len(s0) < S0_SIZE:
        s0.append(nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 4
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    if choice == 'pushb0':
      if len(s0) < S0_SIZE:
        s0.insert(0, nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 6
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'pushf1':
      if len(s1) < S1_SIZE:
        s1.append(nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 5
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'pushb1':
      if len(s1) < S1_SIZE:
        s1.insert(0, nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 7
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'popf0':
      if len(s0) > 0:
        s0.pop()

      dut.uio_in.value = 8
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'popb0':
      if len(s0) > 0:
        del s0[0]

      dut.uio_in.value = 10
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'popf1':
      if len(s1) > 0:
        s1.pop()

      dut.uio_in.value = 9
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'popb1':
      if len(s1) > 0:
        del s1[0]

      dut.uio_in.value = 11
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'toggle':
      ss = 1 - ss
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    if choice == 'replacef0':
      if len(s0) > 0:
        s0.pop()
        s0.append(nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 12
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    if choice == 'replaceb0':
      if len(s0) > 0:
        del s0[0]
        s0.insert(0, nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 14
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'replacef1':
      if len(s1) > 0:
        s1.pop()
        s1.append(nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 13
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

    elif choice == 'replaceb1':
      if len(s1) > 0:
        del s1[0]
        s1.insert(0, nextval)

      dut.ui_in.value = nextval
      dut.uio_in.value = 15
      await ClockCycles(dut.clk, 1)
      dut.uio_in.value = ss
      await ClockCycles(dut.clk, 1)

  await ClockCycles(dut.clk, 10)
  dut._log.info("Tests pass")
