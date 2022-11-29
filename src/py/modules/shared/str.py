from src.py.config import StaticConfig

def withPrefix(prefix: str, name: str) -> str:
  return f'{prefix}_{name}'

def withSuffix(sufix: str, name: str) -> str:
  return f'{name}_{sufix}'

def getExtensionElementId(element: str, config: StaticConfig):
  return withSuffix(config['extensionId'], element)
