from typing import Dict
from copy import deepcopy
from .vcpu import VCpu
from .opcode import Opcode

class MipsProgram():
   def __init__(self, opcodes: Dict[int, Opcode]):
      self.is_finished = False
      self.opcodes = opcodes
      self.exe_id = 1

   def next_instruction(self, vcpu: VCpu):
      pc = vcpu.get_pc()

      if pc.value >= len(self.opcodes):
         self.is_finished = True
         return None

      vcpu.set_pc(pc.value + 1)
      copy = deepcopy(self.opcodes[pc.value])
      copy.exe_id = self.exe_id
      self.exe_id += 1
      return copy
