from pathlib import Path

import pytest

from typing import List

from simulator.mips_virtualization.assembler import preprocess, assemble, get_operand
# from simulator.lib.generics.operand import ImmediateOperand, RegisterIndirectOperand, RegisterOperand, DisplacementOperand
from simulator.lib.generics.opcode import Opcode
from simulator.lib.generics.operand import Operand
from simulator.lib.generics.mipsprogram import MipsProgram
from simulator.lib.generics.pipelinestage import PipelineStage
from simulator.lib.generics.pipelineoperations import PipelineOperations
from simulator.lib.generics.addressing_modes import AddressingMode
from simulator.lib.generics.vcpu import VCpu

class StubOperand(Operand):
   def read(self, vcpu: VCpu) -> int:
      pass

   def write(self, value: int, vcpu: VCpu):
      pass

class StubOpcode(Opcode):
   def tick(self, curr_stage_id, vcpu: VCpu) -> List[PipelineOperations]:
      return []

   def operands_required_at_stage(self, curr_stage_id) -> List[Operand]:
      return []

   def output_operands_forwardable(self, curr_stage_id) -> bool:
      return True

   def supported_input_operand_formats(self) -> List[AddressingMode]:
      return []

stage1: PipelineStage = None
stage2: PipelineStage = None
stage3: PipelineStage = None
program: MipsProgram = None
opcode1: StubOpcode = StubOpcode([], [])
opcode2: StubOpcode = StubOpcode([], [])
opcode3: StubOpcode = StubOpcode([], [])
vcpu: VCpu = None

@pytest.fixture(autouse=True)
def pipeline_init():
   global stage1, stage2, stage3, program, vcpu
   stage1 = PipelineStage(0)
   stage2 = PipelineStage(1)
   stage3 = PipelineStage(2)

   stage1.next = stage2
   stage2.prev = stage1
   stage2.next = stage3
   stage3.prev = stage2

   program = MipsProgram({0:opcode1, 1:opcode2, 2:opcode3})

   vcpu = VCpu({}, {}, 99)

class TestPipelineStage():
   def test_flush_recursively_flushes_prev_stages(self):
      stage1.instruction = opcode3
      stage2.instruction = opcode2
      stage3.instruction = opcode1

      stage3.flush()

      assert stage3.instruction.noop
      assert stage2.instruction.noop
      assert stage1.instruction.noop

   def test_is_data_hazard_returns_true_if_next_stage_has_pending_value(self, monkeypatch):
      stage1.instruction = opcode3
      stage2.instruction = opcode2
      stage3.instruction = opcode1

      opcode2.operands.append(StubOperand(1, 'R1'))
      opcode1.output_operands.append(StubOperand(2, 'R1'))

      def mock_forwardable(*args, **kwargs):
         return False

      monkeypatch.setattr(StubOpcode, "output_operands_forwardable", mock_forwardable)

      hazard = stage3.is_data_hazard(opcode2.operands)

      assert hazard

   def test_is_data_hazard_returns_false_if_next_stage_has_fowardable_value(self, monkeypatch):
      stage1.instruction = opcode3
      stage2.instruction = opcode2
      stage3.instruction = opcode1

      opcode2.operands.append(StubOperand(1, 'R1'))
      opcode1.output_operands.append(StubOperand(2, 'R1'))

      def mock_forwardable(*args, **kwargs):
         return True

      monkeypatch.setattr(StubOpcode, "output_operands_forwardable", mock_forwardable)

      hazard = stage3.is_data_hazard(opcode2.operands)

      assert not hazard

   def test_is_data_hazard_returns_false_if_next_stages_do_not_use_register(self, monkeypatch):
      stage1.instruction = opcode3
      stage2.instruction = opcode2
      stage3.instruction = opcode1

      opcode2.operands.append(StubOperand(1, 'R1'))

      def mock_forwardable(*args, **kwargs):
         return True

      monkeypatch.setattr(StubOpcode, "output_operands_forwardable", mock_forwardable)

      hazard = stage3.is_data_hazard(opcode2.operands)

      assert not hazard

   def test_tick_stalls_if_next_stage_already_stalled(self):
      stage3.stalled = True

      stage2.tick(None, None)
      stage1.tick(None, None)

      assert stage2.stalled
      assert stage1.stalled

   def test_tick_fetches_next_instruction_and_loads_if_first_stage(self):
      stage1.tick(program, vcpu)

      assert stage1.instruction == program.opcodes[0]
      assert stage1.instruction.is_executing

   def test_tick_fetches_instruction_from_prev_stage_if_not_first_stage(self):
      inst = program.opcodes[0]
      inst.load()
      stage2.instruction = inst
      
      stage3.tick(program, vcpu)

      assert stage3.instruction == inst

   def test_tick_unloads_instruction_if_last_stage(self):
      inst = program.opcodes[0]
      inst.load()
      stage3.instruction = inst
      stage3.tick(program, vcpu)

      assert not inst.is_executing
