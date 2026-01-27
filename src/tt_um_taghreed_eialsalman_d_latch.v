`default_nettype none

module tt_um_taghreed_eialsalman_d_latch (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire d = ui_in[0];
    wire e = ui_in[1];

    reg q;

    always @(*) 
        begin
            if (e) 
                q = d; //Same as: if (control = 1)
            else
                q = q; // optional, but makes the latch retention clearer to readers
        end

    // All output pins must be assigned. If not used, assign to 0.
    assign uo_out[0] = q;
    assign uo_out[1] = 1'b0;
    assign uo_out[2] = 1'b0; 
    assign uo_out[3] = 1'b0; 
    assign uo_out[4] = 1'b0; 
    assign uo_out[5] = 1'b0; 
    assign uo_out[6] = 1'b0; 
    assign uo_out[7] = 1'b0;

    assign uio_out = 0;
    assign uio_oe  = 0;

    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, ui_in[7:2], uio_in, 1'b0};

endmodule
