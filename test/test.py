import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, RisingEdge


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
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

    dut._log.info("Test project behavior")

    # Set initial values
    dut.ui_in[0].value = 0  # d
    dut.ui_in[1].value = 0  # e

    # Start toggling d and e
    cocotb.start_soon(toggle_signal(dut, index=0, period_ns=50))  # d = ui_in[0]
    cocotb.start_soon(toggle_signal(dut, index=1, period_ns=30))  # e = ui_in[1]

    # Wait for a few clock cycles
    await ClockCycles(dut.clk, 1000)

    # Example assertion (adjust according to your design)
    # assert dut.uo_out.value == 50, "Output assertion not required"


async def toggle_signal(dut, index, period_ns):
    """Toggle ui_in[index] every period_ns nanoseconds."""
    dut.ui_in[index].value = 0
    while True:
        await Timer(period_ns, units="ns")
        dut.ui_in[index].value = not dut.ui_in[index].value
