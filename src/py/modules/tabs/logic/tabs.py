from src.py.config import SingleTabConfig

from src.py.modules.shared.str import withSuffix, getExtensionElementId

def getTabElementId(element: str, config: SingleTabConfig):
  return withSuffix(getExtensionElementId(element, config['staticConfig']), config['id'])
