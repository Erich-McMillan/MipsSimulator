import argparse
from pathlib import Path
import re

import ptvsd
ptvsd.enable_attach()
ptvsd.wait_for_attach()

from input_parser import load_toml, get_code, get_initial_memory_state, get_initial_register_state
from mips_virtualization.assembler import preprocess, assemble
from mips_virtualization.impl.mips_stage import build_8_stage_pipeline
from lib.generics.register import Register
from lib.vcpu_simulator import VCpuSimulator, PipelineLogger
from lib.generics.vcpu import VCpu

def simulate(inputFile: Path, outputFile: Path):
   # load input
   toml_contents = load_toml(inputFile)
   code = get_code(toml_contents)
   registers = get_initial_register_state(toml_contents)
   memory = get_initial_memory_state(toml_contents)

   # preprocess and assemble
   preprocessed_code = preprocess(code.strip().split('\n'))
   assembled_opcodes = assemble(preprocessed_code)

   # construct stages and vcpu model
   MAX_MEMORY_ADDR = 992
   MAX_REGISTER = 31
   # init all undefined registers to 0
   for i in range(0, MAX_REGISTER+1):
      if f'R{i}' not in registers.keys():
         registers[f'R{i}'] = Register(0)
   vcpu = VCpu(registers, memory, 992)
   stages = build_8_stage_pipeline()
   logger = PipelineLogger()

   # simulate
   simulator = VCpuSimulator(vcpu, stages, logger)
   simulator.load_program(assembled_opcodes)
   simulator.simulate()

   # write output to file
   logger.write_to_file(outputFile)

def main():
   parser = argparse.ArgumentParser(
         description="Simulate 8-stage MIPS processor with DADD, SUB, LD, SD, BNEZ instructions."
      )

   subparsers = parser.add_subparsers(help='subcommand help', dest="command")

   simulate_parser = subparsers.add_parser(
         name='simulate',
         help='Run simulation on input and write results to output.'
      )

   simulate_parser.add_argument(
         'input',
         type = Path,
         help = 'Path to first input file.'
      )
   simulate_parser.add_argument(
         'output',
         type = Path,
         help = 'Path to output first input file.'
      )

   exit_parser = subparsers.add_parser(
         name='exit',
         help='Exit simulator.'
      )

   args = parser.parse_args()

   while args.command != 'exit':
      # run the simulation
      simulate(args.input, args.output)

      # get next command
      valid = False
      while not valid:
         args = None
         try:
            # prompt again for inputs
            user_input = re.sub(
               r'\s{1,}',
               ' ',
               input('Please enter the next input/output files (or --help for additional options, \'exit\' to exit immediately)\n').strip()
            ).split(' ')
            args = parser.parse_args(user_input)
            valid = True
         except SystemExit:
            print('')

if __name__ == '__main__':
   main()
