import sys
from typing import List
import re

from mips_virtualization.impl import instructions
from lib.generics.opcode import Opcode
from lib.generics.operand import Operand, RegisterOperand, ImmediateOperand, RegisterIndirectOperand, DisplacementOperand

def preprocess(code: List[str]) -> List[str]:
   """Preprocesses raw assembly code, by removing labels and replacing them with tenative PC values
   """
   # find all label definitions
   labelDefineRegex = r"(\w+)\s{0,}:\s{0,}"

   processedCode = code

   labels = {}
   # for each line determine if it contains label definition
   for idx, line in enumerate(code):
      label = re.search(labelDefineRegex, line)
      if label != None:
         labels[idx] = label.group(1) # store the label name
         processedCode[idx] = line.replace(label.group(0), '') # remove the label definition, no longer needed

   # for each line replace label reference with immediate addressing to the correct PC value (where label was defined)
   for idx, line in enumerate(processedCode):
      for label in labels:
         processedCode[idx] = processedCode[idx].replace(labels[label], f"#{label}")

   return processedCode

def find_opcode(name: str):
   "returns pointer to opcode class, otherwise throws exception"
   instruction_map = {
      'DADD': instructions.Dadd,
      'LD': instructions.Ld,
      'SD': instructions.Sd,
      'BNEZ': instructions.Bnez,
      'SUB': instructions.Sub
   }

   if name in instruction_map.keys():
      return instruction_map[name]

   raise AssertionError(f"opcode {name} not in supported instructions {instruction_map}")

def get_operand(operand_code: str):
   "compiles operand code into operand and returns the operand if the opcode supports it"
   operand_patterns = {
      r'#(\d+)': ImmediateOperand,
      r'(\w+\d{0,})': RegisterOperand,
      r'\((\w+\d{0,})\)': RegisterIndirectOperand,
      r'(\d+)\((\w+\d{0,})\)': DisplacementOperand
   }

   operand_code_trimmed = operand_code.strip()

   operand_obj = None

   for pattern in operand_patterns:
      matchobj = re.match(pattern, operand_code_trimmed)
      if matchobj:
         if matchobj.group(0) == operand_code_trimmed: # only complete matches indicate that we found the right opcode
            operand_cls = operand_patterns[pattern]

            if operand_cls == ImmediateOperand:
               operand_obj = ImmediateOperand(int(matchobj.group(1)))
            elif operand_cls == RegisterOperand:
               operand_obj = RegisterOperand(matchobj.group(1))
            elif operand_cls == RegisterIndirectOperand:
               operand_obj = RegisterIndirectOperand(matchobj.group(1))
            elif operand_cls == DisplacementOperand:
               operand_obj = DisplacementOperand(matchobj.group(2), int(matchobj.group(1)))

   if operand_obj is None:
      raise AssertionError(f"\"{operand_code}\" invalid syntax")

   return operand_obj

def assemble(preprocessedCode: List[str]) -> List[Opcode]:
   "Compiles preprocessed code and returns the opcodes"
   opcode_pattern = r"(\w+)\s+"
   operand_pattern = r"([\w\d\(\)\#]+)"

   compiled_code = {}
   opcode_id = 0

   for line in preprocessedCode:
      trimmed_line = line.strip()
      
      try:
         # determine the opcode
         opcode = re.match(opcode_pattern, trimmed_line)
         opcode_pntr = find_opcode(opcode.group(1))
         trimmed_line = trimmed_line.replace(opcode.group(0), '')

         # determine it's operands
         operand_code = re.findall(operand_pattern, trimmed_line)
         operands = []
         for op in operand_code:
            operands.append(get_operand(op))

         # add operands to opcode to determine if supported
         compiled_code[opcode_id] = opcode_pntr(operands)
         opcode_id += 1

      except AssertionError as e:
         print(f"Source Error line: \"{line}\"")
         print(e)
         sys.exit()

   return compiled_code

