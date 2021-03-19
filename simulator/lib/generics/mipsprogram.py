from typing import Dict
from .vcpu import VCpu
from .opcode import Opcode

class MipsProgram():
   def __init__(self, opcodes: Dict[int, Opcode]):
      self.is_finished = False
      self.opcodes = opcodes

   def next_instruction(self, vcpu: VCpu):
      pc = vcpu.get_pc()
      pc_next = pc
      pc_next.value= pc_next.value + 1
      vcpu.set_pc(pc_next)

      if pc.value >= len(self.opcodes)-1:
         self.is_finished = True
         return None

      return self.opcodes[pc.value]

   def get_instruction_id(self, opcode: Opcode):
      for key in self.opcodes:
         if self.opcodes[key] == opcode:
            return key
