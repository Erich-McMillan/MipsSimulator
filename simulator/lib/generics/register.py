# from opcode import Opcode

class Register():
   def __init__(self, name: str, value: int):
      self.name = name
      self._value = value
