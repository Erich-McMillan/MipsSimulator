from typing import Dict
from generics.opcode import Opcode
from generics.vcpu import VCpu
from generics.pipelinestage import PipelineStage

class VCpuSimulator():
   def __init__(self, vcpu: VCpu, stages: Dict[PipelineStage]):
      self.vcpu = vcpu
      self.stages = stages

   def load_program(self, opcodes: Dict[Opcode]):
      self.program = opcodes
      # TODO: validate instructions are compatible with vcpu loaded

   def simulate(self, max_cycles=100):
      for stage in self.stages:
         stage.tick(self.program, self.vcpu)
