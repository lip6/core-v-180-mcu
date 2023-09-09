(* blackbox = 1 *)
module pPLL02F (
	RST_N,
	CK_AUX_IN,
	CK_XTAL_IN,
	PRESCALE,
	SSC_EN,
	SSC_STEP,
	SSC_PERIOD,
	INTEGER_MODE,
	MUL_INT,
	MUL_FRAC,
	LOCKED,
	LDET_CONFIG,
	LF_CONFIG,
	PS0_EN,
	PS0_BYPASS,
	PS0_L1,
	PS0_L2,
	CK_PLL_OUT0,
	PS1_EN,
	PS1_BYPASS,
	PS1_L1,
	PS1_L2,
	CK_PLL_OUT1,
	SCAN_IN,
	SCAN_CK,
	SCAN_EN,
	SCAN_MODE,
	SCAN_OUT
);
	input wire RST_N;
	input wire CK_AUX_IN;
	input wire CK_XTAL_IN;
	input wire [3:0] PRESCALE;
	input wire SSC_EN;
	input wire [7:0] SSC_STEP;
	input wire [10:0] SSC_PERIOD;
	input wire INTEGER_MODE;
	input wire [10:0] MUL_INT;
	input wire [11:0] MUL_FRAC;
	output wire LOCKED;
	input wire [8:0] LDET_CONFIG;
	input wire [34:0] LF_CONFIG;
	input wire PS0_EN;
	input wire PS0_BYPASS;
	input wire [1:0] PS0_L1;
	input wire [7:0] PS0_L2;
	output wire CK_PLL_OUT0;
	input wire PS1_EN;
	input wire PS1_BYPASS;
	input wire [1:0] PS1_L1;
	input wire [7:0] PS1_L2;
	output wire CK_PLL_OUT1;
	input wire SCAN_IN;
	input wire SCAN_CK;
	input wire SCAN_EN;
	input wire SCAN_MODE;
	output wire SCAN_OUT;
	reg clk;
	reg clkInternal;
	wire clkOut;
	reg [7:0] counter;
endmodule
