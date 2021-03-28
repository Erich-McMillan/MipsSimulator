from typing import List

from lib.generics.opcode import Opcode, split_in_out_operands
from lib.generics.opcode import Operand
from lib.generics.addressing_modes import AddressingMode
from lib.generics.vcpu import VCpu
import lib.generics.vcpu as vcpulib
from lib.generics.pipelineoperations import PipelineOperations

from .mips_stage import MipsStage

class Bnez(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 0, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def operands_required_at_stage(self, curr_stage_id: MipsStage) -> List[Operand]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.ID:
         return [self.operands[1]] # target instruction addr required at decode
      elif curr_stage_id == MipsStage.EX:
         return [self.operands[0]] # branch condition required at execute
      return []

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      # Bnez is special case, it has no outputs so they are always
      # fowardable
      # IF we were to predict that branches were taken then we would
      # have to force stall the pipeline until we could determine the
      # exact jump addr. In this case the address could be calculated
      # at the end of decode stage
      True

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.RegisterDirect, AddressingMode.Immediate]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.ID:
         self.target_instruction_addr = self.operands[1].read(vcpu)
      # if curr_stage_id == MipsStage.EX:
      if curr_stage_id == MipsStage.MEM1:
         instruction_taken = self.operands[0].read(vcpu)
         if instruction_taken != 0: # branch taken when not zero, pipeline must be flushed
            vcpu.set_register(vcpulib.REG_PROGRAM_COUNTER, self.target_instruction_addr) # set the next instruction counter to the resolved PC
            return [PipelineOperations.Flush] # flush pipeline if we are taking the branch
      return []

class Dadd(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 1, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def operands_required_at_stage(self, curr_stage_id: MipsStage) -> List[Operand]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.EX:
         return self.operands
      return []

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      if self.noop:
         return True
      return curr_stage_id > MipsStage.EX

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.Immediate, AddressingMode.RegisterDirect]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.EX:
         add = self.operands[0].read(vcpu) + self.operands[1].read(vcpu) # a + b
         self.output_operands[0].write(add, vcpu) # -> c
      return []

class Ld(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(1, 1, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def operands_required_at_stage(self, curr_stage_id: MipsStage) -> List[Operand]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.MEM2:
         return self.operands
      return []

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      if self.noop:
         return True
      return curr_stage_id > MipsStage.MEM2

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.RegisterIndirect, AddressingMode.Displacement]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.MEM2:
         mem_val = self.operands[0].read(vcpu)
         self.output_operands[0].write(mem_val, vcpu)
      return []

class Sd(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 0, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def operands_required_at_stage(self, curr_stage_id: MipsStage) -> List[Operand]:
      if curr_stage_id == MipsStage.MEM2:
         return self.operands
      return []

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      # Store is unique in this 8 stage pipeline since subsequent
      # stages never need to stall waiting for data to be written
      # before it can be read, since data can be read after being
      # written in the same cycle and we can only execute 1 thread
      # at a time, this could become an issue in multithreaded 
      # implementations
      return True 

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.RegisterIndirect, AddressingMode.Displacement, AddressingMode.RegisterDirect]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.MEM2:
         mem_val = self.operands[0].read(vcpu)
         self.operands[1].write(mem_val, vcpu)
      return []

class Sub(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 1, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def operands_required_at_stage(self, curr_stage_id: MipsStage) -> List[Operand]:
      if curr_stage_id == MipsStage.EX:
         return self.operands
      return []

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      if self.noop:
         return True
      return curr_stage_id > MipsStage.EX

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.Immediate, AddressingMode.RegisterDirect]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      if self.noop:
         return []
      if curr_stage_id == MipsStage.EX:
         sub = self.operands[0].read(vcpu) - self.operands[1].read(vcpu) # a + b
         self.output_operands[0].write(sub, vcpu) # -> c
      return []
