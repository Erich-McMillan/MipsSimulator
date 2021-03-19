from typing import List, Dict
from pathlib import Path
import toml
from lib.generics.register import Register

def load_toml(path: Path) -> dict:
   return toml.load(path)

def get_initial_memory_state(tomlContents: dict) -> dict:
   MEMORY_KEY = 'memory'

   memory = {}
   initial_memory_values = tomlContents[MEMORY_KEY]

   for key in initial_memory_values:
      memory[int(key)] = initial_memory_values[key]

   return memory

def get_initial_register_state(tomlContents: dict) -> Dict[str, Register]:
   REGISTER_KEY = 'registers'
   
   registers = {}
   initial_register_values = tomlContents[REGISTER_KEY]

   for key in initial_register_values:
      registers[key] = Register(initial_register_values[key])

   return registers

def get_code(tomlContents: dict) -> List[str]:
   CODE_KEY = 'code'
   return tomlContents[CODE_KEY]['code']
