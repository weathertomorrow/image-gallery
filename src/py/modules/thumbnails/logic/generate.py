from PIL import Image
from os import DirEntry, path

from src.py.config import TabConfig

from src.py.modules.shared.names import getThumbnailNameFromImageName

def generateThumbnail(tabConfig: TabConfig, forImage: DirEntry[str]):
  thumbnailSize = tabConfig["staticConfig"]["thumbnails"]["maxSize"]

  image = Image.open(forImage.path)
  image.thumbnail((thumbnailSize, thumbnailSize))
  image.save(path.join(tabConfig["thumbnailsPath"], getThumbnailNameFromImageName(tabConfig, forImage.name)))
