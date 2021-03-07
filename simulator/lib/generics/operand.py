from abc import ABC, abstractmethod

class Operand(ABC):
   @abstractmethod
   def resolve(self, registers: dict) -> int:
      pass
