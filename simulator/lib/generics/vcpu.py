from typing import List, Dict
from .register import Register

REG_PROGRAM_COUNTER = 'PC'

class VCpu():
   def __init__(self, registers: Dict[str, Register], memory: Dict[int, int], max_memory: int):
      # convert registers list into a dict
      self.registers = registers
      self.registers[REG_PROGRAM_COUNTER] = Register(0)
      self.memory = memory
      self.max_mem_addr = max_memory

   def set_pc(self, value):
      self.registers[REG_PROGRAM_COUNTER] = Register(value)

   def get_pc(self) -> int:
      return self.registers[REG_PROGRAM_COUNTER]

   def get_register(self, name: str) -> Register:
      return self.registers[name]

   def set_register(self, name: str, value: int):
      self.registers[name] = Register(value)

   def get_memory_value(self, addr: int) -> int:
      if addr in self.memory.keys():
         return self.memory[addr]
      return 0

   def set_memory_value(self, addr: int, value: int):
      if addr <= self.max_mem_addr:
         self.memory[addr] = value
      else:
         raise AssertionError(f"Memory writeback to invalid memory address {addr}")
