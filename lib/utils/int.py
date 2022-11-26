from typing import Union

def strToNullableInt(arg: str) -> Union[None, int]:
  try:
      num = int(arg)
      return num
  except:
      return None
