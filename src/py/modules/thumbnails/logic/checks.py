from os import DirEntry

from src.py.config import TabConfig
from src.py.modules.shared.names import getThumbnailNameFromImageName
from src.py.modules.thumbnails.logic.types import GetImagesWithMissingThumbnailsOutput

def makeIsMissingThumbnail(tabConfig: TabConfig, allThumbnails: dict[str, None]):
  def isMissingThumbnail(image: DirEntry[str]) -> bool:
    return getThumbnailNameFromImageName(tabConfig, image.name) not in allThumbnails
  return isMissingThumbnail

def isMissingThumbnails(output: GetImagesWithMissingThumbnailsOutput) -> bool:
  return len(output["output"]) != 0
