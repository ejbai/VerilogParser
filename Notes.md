Module definition formats that have been accounted for:

- all inputs and outputs defined in the first line

```
module half_adder(input a, b, output s0, c0);
```

- no inputs or outputs defined in the first line

```
module rams_sp_rom (clk, we, addr, di, dout);

--OR--

module arbiter (
clock      , // clock
reset      , // Active high, syn reset
req_0      , // Request 0
req_1      , // Request 1
gnt_0      , // Grant 0
gnt_1        // Grant 1
);
```

- multiple types of either input or output (different bit widths)

```
module RCA4(output [3:0] sum, output cout, input [3:0] a, b, input cin);
```

- multi-line and multiple types of either input or output

```
module SkipLogic(output cin_next,
  input [3:0] a, b, input cin, cout);
```

- parameters; inputs and outputs defined in an uncommon way

```
module spi_lite
//-----------------------------------------------------------------
// Params
//-----------------------------------------------------------------
#(
     parameter C_SCK_RATIO      = 32
)
//-----------------------------------------------------------------
// Ports
//-----------------------------------------------------------------
(
    // Inputs
     input          clk_i
    ,input          rst_i
    ,input          cfg_awvalid_i
    ,input  [31:0]  cfg_awaddr_i
...
```

Shortcomings and predicted errors:

Firstly, there are likely many different cases I didn't catch, where someone codes in a way that is somewhat unconventional and has a format I didn't account for. A way to combat this would be to rewrite the program in a way that doesn't parse in a traditional manner, but instead looks at the whole thing and interprets it intelligently, and then takes out the pieces based on what it has found. This is pretty much describing some kind of machine learning algorithm.

However, here's what I've noticed so far:

- Does not account for instantiations of a module inside of another module.

- Does not add space between a second bit width specifier if there is one.
