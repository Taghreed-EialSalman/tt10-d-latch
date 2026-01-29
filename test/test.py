import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_d_latch(dut):
    dut._log.info("Start D-latch test")

    # Tiny Tapeout clock (keep)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Tiny Tapeout reset sequence (keep)
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # Mapping (matches your Verilog)
    D = dut.ui_in[0]     # d
    E = dut.ui_in[1]     # e (enable)
    Q = dut.uo_out[0]    # q

    # --- Test 1: Transparent when E=1 (Q follows D) ---
    E.value = 1
    D.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(Q.value) == 0, "Fail: E=1, D=0 => Q must be 0"

    D.value = 1
    await ClockCycles(dut.clk, 2)
    assert int(Q.value) == 1, "Fail: E=1, D=1 => Q must be 1"

    # --- Test 2: Hold when E=0 (Q must not change even if D changes) ---
    E.value = 0
    await ClockCycles(dut.clk, 2)

    D.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(Q.value) == 1, "Fail: E=0, D changed => Q must hold previous value (1)"

    D.value = 1
    await ClockCycles(dut.clk, 2)
    assert int(Q.value) == 1, "Fail: E=0, D changed again => Q must still hold (1)"

    # --- Test 3: Re-enable updates again ---
    E.value = 1
    D.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(Q.value) == 0, "Fail: Re-enable E=1 => Q must update to D"

    dut._log.info("All D-latch tests passed ✅")
