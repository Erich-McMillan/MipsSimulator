from abc import ABC
from typing import List
from .opcode import Opcode
from .register import Register
from .vcpu import VCpu, REG_PROGRAM_COUNTER
from .pipelineoperations import PipelineOperations
from .mipsprogram import MipsProgram
from .opcode import Opcode
from .operand import Operand

class PipelineStage():
   def __init__(self, stage_id: int):
      self.stage_id = stage_id
      self._next: 'PipelineStage' = None
      self._prev: 'PipelineStage' = None
      self.stalled: bool = False
      self._instruction: Opcode = None

   @property
   def next(self) -> 'PipelineStage':
      return self._next

   @next.setter
   def next(self, next):
      self._next = next

   @property
   def prev(self) -> 'PipelineStage':
      return self._prev

   @prev.setter
   def prev(self, prev):
      self._prev = prev

   @property
   def instruction(self) -> Opcode:
      return self._instruction

   @instruction.setter
   def instruction(self, instruction: Opcode):
      self._instruction = instruction

   def is_data_hazard(self, operands: List[Operand]) -> bool:
      """Recurse through all next stages in pipeline to determine if their instruction
      possibly produces an output this current instruction depends upon and returns True
      if the operands cannot be forwarded to the current instruction

      Inputs:
         registers: list of registers to evaluate for hazards in instructions which are 
            further along in pipeline.

      Returns:
         True if hazard exists, False if no hazard
      """
      if self.instruction is not None:
         for operand in operands:
            if operand in self.instruction.output_operands and not self.instruction.output_operands_forwardable(self.stage_id):
               return True

      if self.next == None:
         return False

      return self.next.is_data_hazard(operands)
   
   def flush(self):
      """Flush the pipeline starting with this stage
      """

      if self.instruction != None:
         self.instruction.noop = True

      if self.prev is None:
         return # early return if no previous stages
      
      self.prev.flush()

   def check_for_upstream_stalls(self):
      if self.next != None:
         if self.next.stalled:
            self.stalled = True # stall if the next instruction is stalled

   def fetch_next_instruction(self, program: MipsProgram, vcpu: VCpu):
      if self.stalled:
         return

      if self.next == None: # end of pipeline should unload the instruction it executed last time
         if self.instruction != None:
            self.instruction.unload()
      if self.prev is None: # beginning of pipeline must fetch instruction from PC
         self.instruction = program.next_instruction(vcpu)
         if self.instruction != None:
            self.instruction.load()
      else:
         self.instruction = self.prev.instruction

   def handle_operations(self, operations):
      if PipelineOperations.Flush in operations:
         self.flush()

   def stall_for_hazards(self):
      if self.next is None: # end of pipeline can't have data hazards
         return
      if self.instruction is not None:
         self.stalled = self.next.is_data_hazard(self.instruction.operands_required_at_stage(self.stage_id))

   def execute_instruction(self, program, vcpu):
      if self.stalled == False and self.instruction != None:
         return self.instruction.tick(self.stage_id, vcpu)
      return []

   def tick(self, program: MipsProgram, vcpu: VCpu):
      operations = []
      self.check_for_upstream_stalls()
      self.fetch_next_instruction(program, vcpu)
      self.stall_for_hazards()
      operations = self.execute_instruction(program, vcpu)
      self.handle_operations(operations)

   def reset(self):
      self.stalled = False
      self.instruction = None
