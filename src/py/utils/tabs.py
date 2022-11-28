from src.py.config import TabConfig

from src.py.utils.str import withSuffix

def getTabElementId(element: str, config: TabConfig):
  return withSuffix(withSuffix(config['staticConfig']['extensionId'], element), config['id'])
