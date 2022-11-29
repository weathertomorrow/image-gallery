from src.py.config import TabConfig

def getThumbnailNameFromImageName(tabConfig: TabConfig, imageName: str) -> str:
  return tabConfig["staticConfig"]["thumbnails"]["filePrefix"] + imageName

def getImageNameFromThumbnailName(tabConfig: TabConfig, thumbnailName: str) -> str:
  return thumbnailName.replace(tabConfig["staticConfig"]["thumbnails"]["filePrefix"], '')
