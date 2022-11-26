def isNotEmpty(arg) -> bool:
  return arg != "" and arg != None

def isEmpty(arg) -> bool:
  return not isNotEmpty(arg)
