from pathlib import Path

import pytest

from simulator.input_parser import load_toml, get_initial_memory_state, get_initial_register_state, get_code

sample_toml_path = "test.toml"
sample_code = """
         LD R2, 0(R1)
         DADD R4, R2, R3
         SD R4, 0(R1)
         BNEZ R4, NEXT
         DADD R2, R1, #8
   NEXT: DADD R1, R1, R3
   """
sample_toml = '''
[registers]
   R1=16
   R3=42
   R5=8

[memory]
   8 = 40
   16 = 60

[code]
   code = """
         LD R2, 0(R1)
         DADD R4, R2, R3
         SD R4, 0(R1)
         BNEZ R4, NEXT
         DADD R2, R1, #8
   NEXT: DADD R1, R1, R3
   """
'''

@pytest.fixture(autouse=True)
def setup_module():
   with open(sample_toml_path, "w") as f:
         f.write(sample_toml)

@pytest.fixture(autouse=True)
def teardown_module():
   yield()
   Path(sample_toml_path).unlink()

@pytest.fixture
def toml_data():
   return load_toml(Path(sample_toml_path))

# class TestLoadToml():
#    def test_load(self):
#       toml_contents = load_toml(Path(sample_toml_path))

class TestLoadMemoryState:
   def test_get_initial_register_state(self, toml_data):
      memory = get_initial_memory_state(toml_data)

      assert len(memory) == 2
      assert memory[8] == 40
      assert memory[16] == 60

class TestLoadRegisterState:
   def test_get_initial_memory_state(self, toml_data):
      registers = get_initial_register_state(toml_data)

      assert len(registers) == 3
      assert registers[0].name == 'R1'
      assert registers[0].value == 16
      assert registers[1].name == 'R3'
      assert registers[1].value == 42
      assert registers[2].name == 'R5'
      assert registers[2].value == 8

class TestLoadCode:
   def test_get_code(self, toml_data):
      code = get_code(toml_data)

      assert code.strip() == sample_code.strip()
