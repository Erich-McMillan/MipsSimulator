from abc import ABC, abstractmethod
from typing import Dict, List
from register import Register
from pipelinestage import PipelineStage
from operand import Operand

class Opcode(ABC):
   def __init__(self, operands: List[Operand], output_operands: List[Operand]):
      self.operands = operands
      self.output_operands = output_operands # recipients list will be depleted as they are written
      self.is_executing = False
      self.stalled = False
      self.noop = False

   @abstractmethod
   def output_operands_forwardable(self) -> bool:
      # implementation specific per opcode
      pass

   def unload(self):
      self.is_executing = False
      self.stage = None
      self.stalled = False
      self.noop = False

   def invalidate(self):
      self.noop = True

