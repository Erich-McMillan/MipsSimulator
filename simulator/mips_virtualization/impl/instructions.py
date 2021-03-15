from typing import List

from simulator.lib.generics.opcode import Opcode, split_in_out_operands
from simulator.lib.generics.opcode import Operand
from simulator.lib.generics.addressing_modes import AddressingMode
from simulator.lib.generics.vcpu import VCpu
from simulator.lib.generics.pipelineoperations import PipelineOperations

from .mips_stage import MipsStage

class Bnez(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 0, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      pass

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.RegisterDirect, AddressingMode.Immediate]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      # implementation specific per opcode
      pass

class Dadd(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 1, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      pass

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.Immediate, AddressingMode.RegisterDirect]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      # implementation specific per opcode
      pass

class Ld(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 0, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      pass

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.RegisterDirect, AddressingMode.RegisterIndirect, AddressingMode.Immediate, AddressingMode.Displacement]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      # implementation specific per opcode
      pass

class Sd(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 0, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      pass

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.RegisterDirect, AddressingMode.RegisterIndirect, AddressingMode.Immediate, AddressingMode.Displacement]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      # implementation specific per opcode
      pass

class Sub(Opcode):
   def __init__(self, operands: List[Operand]):
      in_ops, out_ops = split_in_out_operands(2, 1, operands)
      Opcode.__init__(self, in_ops, out_ops)

   def output_operands_forwardable(self, curr_stage_id: MipsStage):
      pass

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return [AddressingMode.Immediate, AddressingMode.RegisterDirect]

   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      # implementation specific per opcode
      pass
