from typing import Dict, List
from pathlib import Path
from lib.generics.opcode import Opcode
from lib.generics.vcpu import VCpu
from lib.generics.pipelinestage import PipelineStage
from lib.generics.mipsprogram import MipsProgram

class PipelineLogger():
   def __init__(self):
      self.logs = []
      self.registers = []
      self.memory = []

   def log(self, cycle: int, program: MipsProgram, stages: List[PipelineStage]):
      spew_string = f"c#{cycle} "

      for stage in stages:
         if stage.instruction != None:
            if not stage.instruction.noop:
               inst_id = stage.instruction.exe_id
               stage_str = ""
               if stage.stalled:
                  stage_str = "stall"
               else:
                  stage_str = stage.stage_id.name
               spew_string += f"I{inst_id}-{stage_str} "

      self.logs.append(spew_string + '\n')

   def log_registers(self, vcpu: VCpu):
      for reg_key in vcpu.registers:
         if reg_key != 'PC' and vcpu.registers[reg_key].value != 0:
            self.registers.append(f"{reg_key} {vcpu.registers[reg_key].value}\n")

   def log_memory(self, vcpu: VCpu):
      for mem_key in vcpu.memory:
         self.memory.append(f"{mem_key} {vcpu.memory[mem_key]}\n")

   def write_to_file(self, filepath: Path):
      with open(filepath, 'w') as f:
         f.writelines(self.logs)
         f.write('REGISTERS\n')
         f.writelines(self.registers)
         f.write('MEMORY\n')
         f.writelines(self.memory)

class VCpuSimulator():
   def __init__(self, vcpu: VCpu, stages: List[PipelineStage], logger: PipelineLogger):
      self.vcpu = vcpu
      self.stages = stages
      self.logger = logger

   def load_program(self, opcodes: Dict[int, Opcode]):
      self.program = MipsProgram(opcodes)

   def pipeline_finished(self) -> bool:
      for stage in self.stages:
         if stage.instruction != None:
            if not stage.instruction.noop:
               return False
      return True

   def simulate(self, max_cycles=30):
      cycle = 1
      try:
         reversed_stages = self.stages
         reversed_stages.reverse()
         firstround = True
         while (firstround or not self.pipeline_finished()) and cycle < max_cycles:
            firstround = False
            for stage in reversed_stages:
               stage.tick(self.program, self.vcpu)
            # log cycle
            if not self.pipeline_finished():
               self.logger.log(cycle, self.program, self.stages)
            cycle = cycle + 1

         # log final reg/mem states
         self.logger.log_memory(self.vcpu)
         self.logger.log_registers(self.vcpu)

      except:
         # print current state of all items
         print(self.logger.logs)
         print(self.vcpu.registers)
         print(self.vcpu.memory)
         raise
