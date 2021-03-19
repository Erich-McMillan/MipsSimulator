from abc import ABC, abstractmethod
from .register import Register
from typing import Dict, List, Tuple
from .operand import Operand
from .addressing_modes import AddressingMode
from .pipelineoperations import PipelineOperations
from .vcpu import VCpu

def split_in_out_operands(num_in, num_out, operands: List[Operand]) -> Tuple[List[Operand], List[Operand]]:
   expected = num_in + num_out
   got = len(operands)
   
   if got < expected:
      raise AssertionError(f"Number of operands is invalid, too few. Expected {expected}, got {got}.")
   if got > expected:
      raise AssertionError(f"Number of operands is invalid, too many. Expected {expected}, got {got}.")

   return (operands[num_out:], operands[0:num_out])

class Opcode(ABC):
   def __init__(self, operands: List[Operand], output_operands: List[Operand]):
      self.operands = operands
      self.output_operands = output_operands
      self.is_executing = False
      self.stalled = False
      self.noop = False
      self.validate_operands()
      self.exe_id = None

   def validate_operands(self):
      for op in self.operands:
         if op.mode not in self.supported_input_operand_formats():
            raise AssertionError(f"Input operand {op} not a supported addressing mode for this instruction. Supported addressing modes {self.supported_input_operand_formats}")

      for op in self.output_operands:
         if op.mode is not AddressingMode.RegisterDirect:
            raise AssertionError(f"Output operand {op} must be register direct addressing mode.")

   @abstractmethod
   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      # implementation specific per opcode
      pass

   @abstractmethod
   def operands_required_at_stage(self, curr_stage_id) -> List[Operand]:
      pass

   @abstractmethod
   def output_operands_forwardable(self, curr_stage_id) -> bool:
      # implementation specific per opcode
      pass

   @abstractmethod
   def supported_input_operand_formats(self) -> List[AddressingMode]:
      # implementation specific per opcode
      pass

   def load(self):
      self.is_executing = True
      self.stalled = False
      self.noop = False

   def unload(self):
      self.is_executing = False
      self.stalled = False
      self.noop = False

   def invalidate(self):
      self.noop = True

