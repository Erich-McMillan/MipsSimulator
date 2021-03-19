from enum import IntEnum
from typing import List

from lib.generics.pipelinestage import PipelineStage

class MipsStage(IntEnum):
   IF1 = 0
   IF2 = 1
   ID = 2
   EX = 3
   MEM1 = 4
   MEM2 = 5
   MEM3 = 6
   WB = 7

def build_8_stage_pipeline() -> List[PipelineStage]:
   stage_ids = [
      MipsStage.IF1,
      MipsStage.IF2,
      MipsStage.ID,
      MipsStage.EX,
      MipsStage.MEM1,
      MipsStage.MEM2,
      MipsStage.MEM3,
      MipsStage.WB
   ]

   stages = []

   for stage_id in stage_ids:
      stages.append(PipelineStage(stage_id))

   # do first stage setup
   stages[0].prev = None
   stages[0].next = stages[1]
   # do middle stages setup
   for i in range(1, 7):
      stages[i].prev = stages[i-1]
      stages[i].next = stages[i+1]
   # do last stage setup
   stages[7].prev = stages[6]
   stages[7].next = None

   return stages
