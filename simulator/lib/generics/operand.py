from abc import ABC, abstractmethod
from typing import List

from .addressing_modes import AddressingMode
from .register import Register

class Operand(ABC):
   def __init__(self, mode):
      self.mode = mode

   @abstractmethod
   def resolve(self, registers: List[Register]) -> int:
      pass

class RegisterOperand(Operand):
   def __init__(self, code: str):
      Operand.__init__(self, AddressingMode.RegisterDirect)

   def resolve(self, registers: List[Register]) -> int:
      pass

class RegisterIndirectOperand(Operand):
   def __init__(self, code: str):
      Operand.__init__(self, AddressingMode.RegisterIndirect)

   def resolve(self, registers: List[Register]) -> int:
      pass

class DisplacementOperand(Operand):
   def __init__(self, code: str):
      Operand.__init__(self, AddressingMode.Displacement)

   def resolve(self, registers: List[Register]) -> int:
      pass
   
class ImmediateOperand(Operand):
   def __init__(self, code: str):
      Operand.__init__(self, AddressingMode.Immediate)

   def resolve(self, registers: List[Register]) -> int:
      pass
