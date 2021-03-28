from enum import IntEnum

class AddressingMode(IntEnum):
   Immediate = 0
   RegisterDirect = 1
   RegisterIndirect = 2
   Displacement = 3
