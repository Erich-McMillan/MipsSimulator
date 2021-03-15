from pathlib import Path

import pytest

from simulator.mips_virtualization.assembler import preprocess, assemble, get_operand
from simulator.lib.generics.operand import ImmediateOperand, RegisterIndirectOperand, RegisterOperand, DisplacementOperand
from simulator.mips_virtualization.impl.instructions import Dadd, Sd, Bnez

sample_code_1label_1ref = [
         "LD R2, 0(R1)",
         "DADD R4, R2, R3",
         "SD R4, 0(R1)",
         "BNEZ R4, NEXT",
         "DADD R2, R1, #8",
   "NEXT: DADD R1, R1, R3"
]

sample_code_1label_2ref = [
         "LD R2, 0(R1)",
         "DADD R4, R2, R3",
         "SD R4, 0(R1)",
         "BNEZ R4, NEXT",
         "DADD R2, R1, #8",
         "BNEZ R4, NEXT",
   "NEXT: DADD R1, R1, R3"
]

sample_code_2label_2ref = [
         "LD R2, 0(R1)",
         "DADD R4, R2, R3",
   "LAST: SD R4, 0(R1)",
         "BNEZ R4, NEXT",
         "DADD R2, R1, #8",
         "BNEZ R4, LAST",
   "NEXT: DADD R1, R1, R3"
]

class TestPreprocess():
   def test_preprocess_single_label(self):
      processed_code = preprocess(sample_code_1label_1ref)
      assert "BNEZ R4, #5" in processed_code

   def test_preprocess_single_label_multiple_references(self):
      processed_code = preprocess(sample_code_1label_2ref)
      assert "BNEZ R4, #6" == processed_code[3]
      assert "BNEZ R4, #6" == processed_code[5]

   def test_preprocess_multiple_label(self):
      processed_code = preprocess(sample_code_2label_2ref)
      assert "BNEZ R4, #6" == processed_code[3]
      assert "BNEZ R4, #2" == processed_code[5]

class TestGetOperand():
   def test_get_operand_immediate_addr(self):
      operand_pntr = get_operand('#2')

      assert operand_pntr != None
      assert type(operand_pntr) == ImmediateOperand

   def test_get_operand_register_addr(self):
      operand_pntr = get_operand('R1')

      assert operand_pntr != None
      assert type(operand_pntr) == RegisterOperand

   def test_get_operand_register_indirect_addr(self):
      operand_pntr = get_operand('(R2)')

      assert operand_pntr != None
      assert type(operand_pntr) == RegisterIndirectOperand

   def test_get_operand_displacement_addr(self):
      operand_pntr = get_operand('10(R5)')

      assert operand_pntr != None
      assert type(operand_pntr) == DisplacementOperand

class TestAssembler():
   def test_assemble_register_addressing(self):
      asm_code = assemble(["DADD R4, R2, R3"])

      assert len(asm_code) != 0
      assert type(asm_code[0]) is Dadd

   def test_assemble_register_indirect_addressing(self):
      asm_code = assemble(["SD R4, (R1)"])

      assert len(asm_code) != 0
      assert type(asm_code[0]) is Sd

   def test_assemble_immediate_addressing(self):
      asm_code = assemble(["SD R4, #2"])

      assert len(asm_code) != 0
      assert type(asm_code[0]) is Sd

   def test_assemble_displacement_addressing(self):
      asm_code = assemble(["SD R4, 3(R1)"])

      assert len(asm_code) != 0
      assert type(asm_code[0]) is Sd

   def test_assemble_program(self):
      asm_code = assemble(["SD R4, 3(R1)", "DADD R4, R2, R3", "BNEZ R4, #3", "DADD R1, R1, R3"])

      assert len(asm_code) == 4
      assert type(asm_code[0]) is Sd
      assert type(asm_code[0].operands[0]) is RegisterOperand
      assert type(asm_code[0].operands[1]) is DisplacementOperand
      assert type(asm_code[1]) is Dadd
      assert type(asm_code[1].operands[0]) is RegisterOperand
      assert type(asm_code[1].operands[1]) is RegisterOperand
      assert type(asm_code[1].output_operands[0]) is RegisterOperand
      assert type(asm_code[2]) is Bnez
      assert type(asm_code[2].operands[0]) is RegisterOperand
      assert type(asm_code[2].operands[1]) is ImmediateOperand
      assert type(asm_code[3]) is Dadd
      assert type(asm_code[3].operands[0]) is RegisterOperand
      assert type(asm_code[3].operands[1]) is RegisterOperand
      assert type(asm_code[3].output_operands[0]) is RegisterOperand
