from typing import List, Dict
from .register import Register

REG_PROGRAM_COUNTER = 'PC'

class VCpu():
   def __init__(self, registers: List[Register], memory: Dict[str, int]):
      # convert registers list into a dict
      self.registers = registers
      self.registers.append(Register(REG_PROGRAM_COUNTER))
      self.memory = memory
