from abc import ABC
from typing import List
from .opcode import Opcode
from .register import Register
from .vcpu import VCpu, REG_PROGRAM_COUNTER
from .pipelineoperations import PipelineOperations
from program import Program

class PipelineStage():
   def __init__(self, stage_id: int):
      self.stage_id = stage_id
      self._next: PipelineStage = None
      self._prev: PipelineStage = None
      self.stalled: bool = False
      self._instruction: Opcode = None
      self.outgoing_instruction: OpCode = None

   @property
   def next(self) -> PipelineStage:
      return self._next

   @next.setter
   def next(self, next):
      self._next = next

   @property
   def prev(self) -> PipelineStage:
      return self._prev

   @prev.setter
   def prev(self, prev):
      self._prev = prev

   @property
   def instruction(self) -> Opcode:
      return self._instruction

   @instruction.setter
   def instruction(self, instruction: OpCode):
      self._instruction = instruction

   def is_data_hazard(self, registers: List[Register]) -> bool:
      """Recurse through all next stages in pipeline to determine if their instruction
      possibly produces an output this current instruction depends upon and returns True
      if the operands cannot be forwarded to the current instruction

      Inputs:
         registers: list of registers to evaluate for hazards in instructions which are 
            further along in pipeline.

      Returns:
         True if hazard exists, False if no hazard
      """
      for register in registers:
         if register in self.instruction.output_operands and not self.instruction.output_operands_forwardable(self.stage_id):
            return False

      if self.next == None:
         return False

      return self.next.is_data_hazard(registers)
   
   def flush(self):
      """Flush the pipeline starting with this stage
      """

      self.instruction.noop = True

      if self.prev is None:
         return # early return if no previous stages
      
      self.prev.flush()

   def tick(self, program: Program, vcpu: VCpu):
      if self.next.stalled:
         self.stalled = True
      else:
         if self.prev is not None: # beginning of pipeline must fetch instruction from PC
            self.instruction = self.prev.instruction
         else:
            self.instruction = program[vcpu.registers[REG_PROGRAM_COUNTER]]

         if self.next is not None: # end of pipeline can't have data hazards
            self.stalled = self.next.is_data_hazard(self.instruction.output_operands)
            self.instruction.unload = False

      if self.stalled == False and self.instruction.is_executing and not self.instruction.noop:
         operations = self.instruction.tick(self.stage_id, vcpu)
         if PipelineOperations.Flush in operations:
            self.flush()

   def reset(self):
      self.stalled = False
      self.instruction = None
      self.outgoing_instruction = None
