from typing import Dict, List
from pathlib import Path
from lib.generics.opcode import Opcode
from lib.generics.vcpu import VCpu
from lib.generics.pipelinestage import PipelineStage
from lib.generics.mipsprogram import MipsProgram

class PipelineLogger():
   def __init__(self):
      self.logs = {}
      self.registers = {}
      self.memory = []

   def log(self, cycle: int, program: MipsProgram, stages: List[PipelineStage]):
      spew_string = f"c#{cycle} "

      for stage in stages:
         if stage.instruction != None:
            if not stage.instruction.noop:
               inst_id = program.get_instruction_id(stage.instruction)
               stage_str = ""
               if stage.stalled:
                  stage_str = "stall"
               else:
                  stage_str = stage.stage_id.name
               spew_string += f"I{inst_id}-{stage_str} "

      self.logs[cycle] = spew_string

   def log_registers(self, vcpu: VCpu):
      self.registers = vcpu.registers

   def log_memory(self, vcpu: VCpu):
      self.memory = vcpu.memory

   def write_to_file(self, filepath: Path):
      print('hi there')

class VCpuSimulator():
   def __init__(self, vcpu: VCpu, stages: List[PipelineStage], logger: PipelineLogger):
      self.vcpu = vcpu
      self.stages = stages
      self.logger = logger

   def load_program(self, opcodes: Dict[int, Opcode]):
      self.program = MipsProgram(opcodes)

   def simulate(self, max_cycles=100):
      cycle = 0
      try:
         reversed_stages = self.stages
         reversed_stages.reverse()
         while not self.program.is_finished:
            for stage in reversed_stages:
               stage.tick(self.program, self.vcpu)
            cycle = cycle + 1
            # log cycle
            self.logger.log(cycle, self.program, self.stages)

         # log final reg/mem states
         self.logger.log_memory(self.vcpu)
         self.logger.log_registers(self.vcpu)

      except:
         # print current state of all items
         print(self.logger.logs)
         print(self.vcpu.registers)
         print(self.vcpu.memory)
         raise
