from src.py.config import TabConfig

from src.py.modules.shared.str import withSuffix, getExtensionElementId

def getTabElementId(element: str, config: TabConfig):
  return withSuffix(getExtensionElementId(element, config['staticConfig']), config['id'])
