from enum import IntEnum

class MipsStage(IntEnum):
   IF1 = 0
   IF2 = 1
   ID = 2
   EX = 3
   MEM1 = 4
   MEM2 = 5
   MEM3 = 6
   WB = 7
