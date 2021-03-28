# 8 Stage Mips Simulator Project

This project simulates an 8 stage MIPS processor with the following instructions:

- DADD
- SUB
- SD
- LD
- BNEZ

The 8 stages are:

1. Fetch1
2. Fetch2
3. Decode
4. Execute
5. Memory1
6. Memory2
7. Memory3
8. Writeback

The features of the MIPS processor are:

- Operand forwarding between all stages
- Hazard stalls
- Predict branch not taken
- R/W to registers in same cycle, first write then read
- Registers 0-31 are supported
- Memory locations 0-999 are supported

The R type instructions (DADD/SUB) require and produce operands at Execute stage.
The L type instructions (SD/LD) require and produce operands at Memory2 stage.
The SB type instructions (BNEZ) require input operands, i.e. branch target address at decode stage, and evaluate the condition then update the PC at Execute stage.

## Using the simulator

### Requirements

The requirements for this project are:

- Python "^3.8"
- Toml "^0.10.2"

Toml can be installed using `pip install toml`

### Running the program

To run the program's argument helper, open a terminal at the root of the project directory and run `python simulator/main.py --help`, this will show:

```ps1
usage: main.py [-h] {simulate,exit} ...

Simulate 8-stage MIPS processor with DADD, SUB, LD, SD, BNEZ instructions.

positional arguments:
  {simulate,exit}  subcommand help
    simulate       Run simulation on input and write results to output.
    exit           Exit simulator.

optional arguments:
  -h, --help       show this help message and exit
```

The simulator accepts two primary commands: simluate and exit. Simulate takes an input file formatted as toml with the following keys:

*sample.toml*

```toml
[registers]
   # a list of initial register values, any non-specified registers will default to 0u
   # list registers by id = initial value
   R1 = 5 # these are decimal values
   R4 = 3

[memory]
   # a list of initial memory values by address,  any non-specified registers will default to 0u
   # list memory locations by address = initial value
   3 = 5 # these are decimal values

[code]
   # your code to simulate goes here in """ """ block
   code = """
         LD R2, (R4)
         DADD R3, R2, R1
   """
```

To run this code the following command can be used: `python simulator/main.py simulate path/to/sample.toml path/to/write/output.txt`. Output.txt will display the final register and memory values of the program plus the stage of each instruction during each cycle of program execution:

*output.txt*
```
c#1 I1-IF1 
c#2 I1-IF2 I2-IF1 
c#3 I1-ID I2-IF2 
c#4 I1-EX I2-ID 
c#5 I1-MEM1 I2-stall 
c#6 I1-MEM2 I2-stall 
c#7 I1-MEM3 I2-EX 
c#8 I1-WB I2-MEM1 
c#9 I2-MEM2 
c#10 I2-MEM3 
c#11 I2-WB 
REGISTERS
R1 5
R4 3
R2 5
R3 10
MEMORY
3 5
```

Once the program has completed the first simulation it will prompt you to enter `simulate path/to/next/input.toml path/to/next/output.txt` exit` to end the program. 
