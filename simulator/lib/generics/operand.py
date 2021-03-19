from abc import ABC, abstractmethod
from typing import List

from .addressing_modes import AddressingMode
from .vcpu import VCpu

class Operand(ABC):
   def __init__(self, mode: AddressingMode, register_id):
      self.register_id = register_id
      self.mode = mode

   @abstractmethod
   def read(self, vcpu: VCpu) -> int:
      pass

   @abstractmethod
   def write(self, value: int, vcpu: VCpu):
      pass

   def __eq__(self, other):
      if isinstance(other, Operand):
         return self.register_id == other.register_id
      return False

class RegisterOperand(Operand):
   def __init__(self, register_id: str):
      Operand.__init__(self, AddressingMode.RegisterDirect, register_id)

   def read(self, vcpu: VCpu) -> int:
      return vcpu.get_register(self.register_id).value

   def write(self, value: int, vcpu: VCpu):
      vcpu.set_register(self.register_id, value)

class RegisterIndirectOperand(Operand):
   def __init__(self, register_id: str):
      Operand.__init__(self, AddressingMode.RegisterIndirect, register_id)

   def calc_addr(self, vcpu: VCpu) -> int:
      return vcpu.get_register(self.register_id).value

   def read(self, vcpu: VCpu) -> int:
      addr = self.calc_addr(vcpu)
      return vcpu.get_memory_value()

   def write(self, value: int, vcpu: VCpu):
      vcpu.set_memory_value(self.calc_addr(vcpu), value)

class DisplacementOperand(Operand):
   def __init__(self, register_id: str, offset: int):
      self.offset = offset
      Operand.__init__(self, AddressingMode.Displacement, register_id)

   def calc_addr(self, vcpu: VCpu) -> int:
      return vcpu.get_register(self.register_id).value + self.offset

   def read(self, vcpu: VCpu) -> int:
      addr = self.calc_addr(vcpu)
      return vcpu.get_memory_value(addr)

   def write(self, value: int, vcpu: VCpu):
      vcpu.set_memory_value(self.calc_addr(vcpu), value)
   
class ImmediateOperand(Operand):
   def __init__(self, value: int):
      self.value = value
      Operand.__init__(self, AddressingMode.Immediate, None)

   def read(self, vcpu: VCpu) -> int:
      return self.value

   def write(self, value: int, vcpu: VCpu):
      raise NotImplementedError("Write not supported for Immediate Addressing")
