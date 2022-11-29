from src.py.config import TabConfig

from src.py.modules.shared.str import withSuffix

def getTabElementId(element: str, config: TabConfig):
  return withSuffix(withSuffix(config['staticConfig']['extensionId'], element), config['id'])
