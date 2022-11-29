from src.py.config import TabConfig
from src.py.modules.shared.str import withPrefix

def getThumbnailNameFromImageName(tabConfig: TabConfig, imageName: str) -> str:
  return withPrefix(tabConfig["staticConfig"]["thumbnails"]["filePrefix"], imageName)

def getImageNameFromThumbnailName(tabConfig: TabConfig, thumbnailName: str) -> str:
  return thumbnailName.replace(tabConfig["staticConfig"]["thumbnails"]["filePrefix"], '')
